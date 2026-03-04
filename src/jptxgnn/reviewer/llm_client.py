"""OpenAI API client for LLM interactions."""

import os
from pathlib import Path


class LLMClient:
    """Client for OpenAI API interactions.

    Uses environment variable OPENAI_API_KEY for authentication.
    """

    def __init__(
        self,
        model: str = "gpt-4o",
        api_key: str | None = None,
    ):
        """Initialize the LLM client.

        Args:
            model: OpenAI model to use (default: gpt-4o)
            api_key: Optional API key. If not provided, uses OPENAI_API_KEY env var.
        """
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY environment variable or pass api_key parameter."
            )

        # Lazy import to avoid dependency issues if openai is not installed
        self._client = None

    @property
    def client(self):
        """Get or create the OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                import httpx

                # Use longer timeout for large prompts
                timeout = httpx.Timeout(600.0, connect=120.0)
                # Use custom http client with retries for SSL issues
                http_client = httpx.Client(
                    timeout=timeout,
                    transport=httpx.HTTPTransport(retries=3),
                )
                self._client = OpenAI(api_key=self.api_key, http_client=http_client)
            except ImportError:
                raise ImportError(
                    "openai package not installed. "
                    "Install with: pip install openai"
                )
        return self._client

    def chat(
        self,
        user_message: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        max_retries: int = 5,
    ) -> str:
        """Send a chat message and get a response.

        Args:
            user_message: The user's message
            system_prompt: Optional system prompt
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            max_retries: Maximum retry attempts for transient errors

        Returns:
            The assistant's response text
        """
        import time

        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": user_message})

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens:
            kwargs["max_tokens"] = max_tokens

        # Import OpenAI exceptions for proper handling
        try:
            from openai import APITimeoutError, APIConnectionError
        except ImportError:
            APITimeoutError = Exception
            APIConnectionError = Exception

        last_error = None
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
            except (APITimeoutError, APIConnectionError) as e:
                last_error = e
                wait_time = min(30 * (2 ** attempt), 120)  # 30s, 60s, 120s, 120s, 120s
                print(f"  [Retry {attempt + 1}/{max_retries}] API error: {type(e).__name__}, waiting {wait_time}s...")
                time.sleep(wait_time)
                # Recreate the client to reset connection
                self._client = None
                continue
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                # Retry on transient network errors
                if any(x in error_str for x in ["timeout", "connection", "disconnected", "eof"]):
                    wait_time = min(30 * (2 ** attempt), 120)  # 30s, 60s, 120s, 120s, 120s
                    print(f"  [Retry {attempt + 1}/{max_retries}] Connection error, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    # Recreate the client to reset connection
                    self._client = None
                    continue
                # Don't retry on other errors
                raise

        # All retries exhausted
        raise last_error

    def chat_with_prompt_file(
        self,
        user_message: str,
        prompt_file: str | Path,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> str:
        """Send a chat message using a system prompt from a file.

        Args:
            user_message: The user's message
            prompt_file: Path to the prompt file (.md or .txt)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response

        Returns:
            The assistant's response text
        """
        prompt_path = Path(prompt_file)
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        system_prompt = prompt_path.read_text(encoding="utf-8")

        return self.chat(
            user_message=user_message,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )


def get_prompt_path(prompt_name: str) -> Path:
    """Get the path to a prompt file.

    Args:
        prompt_name: One of:
            - "evidence_pack_reviewer" - Pair-centric v1
            - "evidence_pack_reviewer_v2" - Drug-centric v2
            - "pharmacist" - Pair-centric pharmacist notes
            - "pharmacist_v2" - Drug-centric pharmacist notes
            - "sponsor" - Pair-centric sponsor notes
            - "sponsor_v2" - Drug-centric sponsor notes

    Returns:
        Path to the prompt file
    """
    base_dir = Path(__file__).parent.parent.parent.parent / "prompts"

    prompt_paths = {
        # Pair-centric (v1) prompts
        "evidence_pack_reviewer": base_dir / "Evidence Pack Reviewer" / "v1.md",
        "pharmacist": base_dir / "Notes Writer" / "pharmacist_v1.md",
        "sponsor": base_dir / "Notes Writer" / "sponsor_v1.md",
        # Drug-centric (v2) prompts
        "evidence_pack_reviewer_v2": base_dir / "Evidence Pack Reviewer" / "v2_drug_centric.md",
        "pharmacist_v2": base_dir / "Notes Writer" / "pharmacist_v2_drug_centric.md",
        "sponsor_v2": base_dir / "Notes Writer" / "sponsor_v2_drug_centric.md",
        # Drug-centric (v3) prompts - with pharmacist feedback
        "pharmacist_v3": base_dir / "Notes Writer" / "pharmacist_v3_drug_centric.md",
        "sponsor_v3": base_dir / "Notes Writer" / "sponsor_v3_drug_centric.md",
        # Drug-centric (v4) prompts - with full Data Gap framework
        "evidence_pack_reviewer_v3": base_dir / "Evidence Pack Reviewer" / "v3_drug_centric.md",
        "pharmacist_v4": base_dir / "Notes Writer" / "pharmacist_v4_drug_centric.md",
        "sponsor_v4": base_dir / "Notes Writer" / "sponsor_v4_drug_centric.md",
        # Drug-centric (v5) prompts - storytelling format
        "pharmacist_v5": base_dir / "pharmacist_v5_storytelling.md",
    }

    if prompt_name not in prompt_paths:
        raise ValueError(
            f"Unknown prompt: {prompt_name}. "
            f"Available: {list(prompt_paths.keys())}"
        )

    return prompt_paths[prompt_name]
