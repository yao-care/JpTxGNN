"""Base class for Notes Writers."""

import json
from abc import ABC, abstractmethod
from pathlib import Path

from ..reviewer.llm_client import LLMClient


class BaseNotesWriter(ABC):
    """Abstract base class for all Notes Writers.

    Notes Writers generate PDF-ready Markdown reports from Evidence Packs.
    """

    writer_type: str = "base"
    prompt_name: str = ""  # Subclasses must override

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        model: str = "gpt-4o",
    ):
        """Initialize the writer.

        Args:
            llm_client: Optional LLMClient instance
            model: Model to use if creating a new LLMClient
        """
        self.llm_client = llm_client or LLMClient(model=model)

    @property
    @abstractmethod
    def prompt_path(self) -> Path:
        """Get the path to the prompt file."""
        pass

    def generate(
        self,
        evidence_pack: dict | str | Path,
        temperature: float = 0.5,
    ) -> str:
        """Generate notes from an Evidence Pack.

        Args:
            evidence_pack: Evidence Pack as dict, JSON string, or file path
            temperature: LLM temperature

        Returns:
            Markdown content for the notes
        """
        # Load evidence pack if it's a file path
        if isinstance(evidence_pack, (str, Path)):
            path = Path(evidence_pack)
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    if path.suffix == ".json":
                        evidence_pack = json.load(f)
                    else:
                        evidence_pack = f.read()

        # Convert dict to JSON string for the prompt
        if isinstance(evidence_pack, dict):
            evidence_json = json.dumps(evidence_pack, indent=2, ensure_ascii=False)
        else:
            evidence_json = evidence_pack

        user_message = f"""請根據以下 Evidence Pack 產生報告：

```json
{evidence_json}
```

請按照指定的章節順序輸出 Markdown 格式的報告。
"""

        response = self.llm_client.chat_with_prompt_file(
            user_message=user_message,
            prompt_file=self.prompt_path,
            temperature=temperature,
        )

        return self._clean_response(response)

    def _clean_response(self, response: str) -> str:
        """Clean up the LLM response.

        Removes markdown code block wrappers if present.
        """
        # Remove markdown code block wrappers
        if response.startswith("```markdown"):
            response = response[len("```markdown"):].strip()
        elif response.startswith("```md"):
            response = response[len("```md"):].strip()
        elif response.startswith("```"):
            response = response[3:].strip()

        if response.endswith("```"):
            response = response[:-3].strip()

        return response

    def generate_and_save(
        self,
        evidence_pack: dict | str | Path,
        output_path: str | Path,
        temperature: float = 0.5,
    ) -> Path:
        """Generate notes and save to a file.

        Args:
            evidence_pack: Evidence Pack as dict, JSON string, or file path
            output_path: Path to save the output file
            temperature: LLM temperature

        Returns:
            Path to the saved file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        content = self.generate(evidence_pack, temperature)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        return output_path
