"""Drug-centric Sponsor Notes Writer."""

from pathlib import Path

from ..reviewer.llm_client import get_prompt_path
from .base import BaseNotesWriter


class DrugSponsorNotesWriter(BaseNotesWriter):
    """Generates Drug Sponsor Notes from Drug Evidence Pack.

    Focus areas (drug-centric):
    - One drug with multiple predicted indications
    - Per-indication evidence strength and development feasibility
    - Priority ranking for indications
    - Taiwan regulatory/market feasibility
    - MVP study suggestions
    """

    writer_type = "drug_sponsor"
    prompt_name = "sponsor_v4"

    @property
    def prompt_path(self) -> Path:
        """Get the path to the drug-centric sponsor prompt file (v4)."""
        return get_prompt_path("sponsor_v4")
