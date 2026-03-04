"""Sponsor Notes Writer."""

from pathlib import Path

from ..reviewer.llm_client import get_prompt_path
from .base import BaseNotesWriter


class SponsorNotesWriter(BaseNotesWriter):
    """Generates Sponsor (Pharma) Notes from Evidence Pack.

    Focus areas:
    - Evidence strength and development feasibility
    - Clinical trial status and gaps
    - Taiwan regulatory feasibility
    - MVP validation proposals
    """

    writer_type = "sponsor"
    prompt_name = "sponsor"

    @property
    def prompt_path(self) -> Path:
        """Get the path to the sponsor prompt file."""
        return get_prompt_path("sponsor")
