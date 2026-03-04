"""Drug-centric Pharmacist Notes Writer."""

from pathlib import Path

from ..reviewer.llm_client import get_prompt_path, LLMClient
from .base import BaseNotesWriter


class DrugPharmacistNotesWriter(BaseNotesWriter):
    """Generates Drug Pharmacist Notes from Drug Evidence Pack.

    Focus areas (drug-centric):
    - One drug with multiple predicted indications
    - Drug-level safety (ADR, contraindications, DDI)
    - Per-indication considerations
    - Monitoring and patient education
    - Taiwan availability
    """

    writer_type = "drug_pharmacist"
    prompt_name = "pharmacist_v4"

    def __init__(
        self,
        llm_client: LLMClient | None = None,
        model: str = "gpt-4o",
        prompt_version: str = "v4",
    ):
        """Initialize the writer.

        Args:
            llm_client: Optional LLMClient instance
            model: Model to use if creating a new LLMClient
            prompt_version: Prompt version to use (v4 or v5)
        """
        super().__init__(llm_client=llm_client, model=model)
        self.prompt_version = prompt_version
        self.prompt_name = f"pharmacist_{prompt_version}"

    @property
    def prompt_path(self) -> Path:
        """Get the path to the pharmacist prompt file."""
        return get_prompt_path(self.prompt_name)
