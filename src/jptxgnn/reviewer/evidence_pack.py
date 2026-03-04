"""Evidence Pack generator using LLM."""

import json
import re
from pathlib import Path

from ..collectors.bundle import EvidenceBundle
from .llm_client import LLMClient, get_prompt_path


class EvidencePackGenerator:
    """Generates Evidence Pack from an EvidenceBundle using LLM.

    Uses the Evidence Pack Reviewer prompt to process the bundle
    and output structured evidence_pack.json and evidence_pack.md.
    """

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        model: str = "gpt-4o",
    ):
        """Initialize the generator.

        Args:
            llm_client: Optional LLMClient instance. If not provided, creates one.
            model: Model to use if creating a new LLMClient.
        """
        self.llm_client = llm_client or LLMClient(model=model)
        self.prompt_path = get_prompt_path("evidence_pack_reviewer")

    def generate(
        self,
        bundle: EvidenceBundle,
        temperature: float = 0.3,
    ) -> tuple[dict, str]:
        """Generate Evidence Pack from a bundle.

        Args:
            bundle: The EvidenceBundle containing collected data
            temperature: LLM temperature (lower = more deterministic)

        Returns:
            Tuple of (evidence_pack_json, evidence_pack_md)
        """
        # Prepare the user message with the bundle data
        user_message = f"""請處理以下爬蟲輸出資料，產生 Evidence Pack：

```json
{bundle.to_json()}
```

請輸出：
1. evidence_pack.json（完整 JSON 結構）
2. evidence_pack.md（摘要文件）
"""

        # Call the LLM
        response = self.llm_client.chat_with_prompt_file(
            user_message=user_message,
            prompt_file=self.prompt_path,
            temperature=temperature,
        )

        # Parse the response
        return self._parse_response(response)

    def _parse_response(self, response: str) -> tuple[dict, str]:
        """Parse LLM response to extract JSON and Markdown.

        Args:
            response: Raw LLM response text

        Returns:
            Tuple of (evidence_pack_json, evidence_pack_md)
        """
        evidence_json = {}
        evidence_md = ""

        # Try to extract JSON from code blocks
        json_pattern = r"```json\s*([\s\S]*?)```"
        json_matches = re.findall(json_pattern, response)

        if json_matches:
            try:
                evidence_json = json.loads(json_matches[0])
            except json.JSONDecodeError:
                # If parsing fails, try to find any valid JSON object
                for match in json_matches:
                    try:
                        evidence_json = json.loads(match)
                        break
                    except json.JSONDecodeError:
                        continue

        # Try to extract Markdown section
        # Look for content after JSON or between markdown code blocks
        md_pattern = r"```markdown\s*([\s\S]*?)```"
        md_matches = re.findall(md_pattern, response)

        if md_matches:
            evidence_md = md_matches[0].strip()
        else:
            # If no markdown block, try to find content after the JSON
            # Split by the last ``` and take what's after
            parts = response.split("```")
            if len(parts) >= 3:
                # Get the last non-JSON part
                for i in range(len(parts) - 1, -1, -1):
                    part = parts[i].strip()
                    if part and not part.startswith("{") and not part.startswith("json"):
                        if "Candidate Snapshot" in part or "Evidence Level" in part:
                            evidence_md = part
                            break

        # If still no markdown, use the whole response minus JSON blocks
        if not evidence_md:
            temp = response
            for match in json_matches:
                temp = temp.replace(f"```json\n{match}\n```", "")
                temp = temp.replace(f"```json{match}```", "")
            evidence_md = temp.strip()

        return evidence_json, evidence_md

    def generate_and_save(
        self,
        bundle: EvidenceBundle,
        output_dir: str | Path,
        temperature: float = 0.3,
    ) -> tuple[Path, Path]:
        """Generate Evidence Pack and save to files.

        Args:
            bundle: The EvidenceBundle containing collected data
            output_dir: Directory to save output files
            temperature: LLM temperature

        Returns:
            Tuple of (json_path, md_path)
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        evidence_json, evidence_md = self.generate(bundle, temperature)

        # Generate filename from candidate info
        drug_slug = bundle.candidate.inn.lower().replace(" ", "_")
        indication_slug = (
            bundle.candidate.indication_raw or "unknown"
        ).lower().replace(" ", "_")[:30]

        base_name = f"{drug_slug}_{indication_slug}"

        # Save JSON
        json_path = output_dir / f"{base_name}_evidence_pack.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(evidence_json, f, indent=2, ensure_ascii=False)

        # Save Markdown
        md_path = output_dir / f"{base_name}_evidence_pack.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(evidence_md)

        return json_path, md_path
