"""Claude Code CLI client for LLM interactions.

Uses `claude -p` (print mode) to invoke the Claude Code CLI as the LLM backend.
No API key required — uses the user's existing Claude Code subscription.
"""

import subprocess
import time
from pathlib import Path


class LLMClient:
    """Client that invokes the claude CLI for LLM interactions.

    No API key required — relies on the user's Claude Code authentication.
    """

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,  # kept for backward compat, ignored
    ):
        """Initialize the LLM client.

        Args:
            model: Optional model override (e.g. "sonnet", "opus").
                   If None, uses Claude Code's default model.
            api_key: Ignored. Kept for backward compatibility.
        """
        self.model = model

    def chat(
        self,
        user_message: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 16384,
        max_retries: int = 3,
    ) -> str:
        """Send a message to claude CLI and get a response.

        Args:
            user_message: The user's message (passed via stdin)
            system_prompt: Optional system prompt (passed via --system-prompt)
            temperature: Unused by CLI, kept for API compatibility
            max_tokens: Unused by CLI, kept for API compatibility
            max_retries: Maximum retry attempts on transient errors

        Returns:
            The assistant's response text
        """
        cmd = [
            "claude", "-p",
            "--output-format", "text",
            "--verbose",
        ]

        if self.model:
            cmd.extend(["--model", self.model])

        if system_prompt:
            cmd.extend(["--system-prompt", system_prompt])

        last_error = None
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    cmd,
                    input=user_message,
                    capture_output=True,
                    text=True,
                    timeout=600,
                )
                if result.returncode != 0:
                    stderr = result.stderr.strip()
                    # Check for transient errors
                    if any(x in stderr.lower() for x in ["overloaded", "timeout", "rate"]):
                        raise RuntimeError(stderr)
                    raise RuntimeError(f"claude CLI failed (exit {result.returncode}): {stderr[:300]}")
                return result.stdout.strip()

            except subprocess.TimeoutExpired as e:
                last_error = e
                wait_time = min(30 * (2 ** attempt), 120)
                print(f"  [Retry {attempt + 1}/{max_retries}] Timeout, waiting {wait_time}s...")
                time.sleep(wait_time)

            except RuntimeError as e:
                last_error = e
                error_str = str(e).lower()
                if any(x in error_str for x in ["overloaded", "timeout", "rate"]):
                    wait_time = min(30 * (2 ** attempt), 120)
                    print(f"  [Retry {attempt + 1}/{max_retries}] {type(e).__name__}, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise

            except Exception as e:
                raise

        raise last_error

    def chat_with_prompt_file(
        self,
        user_message: str,
        prompt_file: str | Path,
        temperature: float = 0.7,
        max_tokens: int = 16384,
    ) -> str:
        """Send a chat message using a system prompt from a file.

        Args:
            user_message: The user's message
            prompt_file: Path to the prompt file (.md or .txt)
            temperature: Unused by CLI, kept for API compatibility
            max_tokens: Unused by CLI, kept for API compatibility

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
