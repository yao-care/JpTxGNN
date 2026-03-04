"""Pharmacist Notes Writer."""

from pathlib import Path

from ..reviewer.llm_client import get_prompt_path
from .base import BaseNotesWriter


class PharmacistNotesWriter(BaseNotesWriter):
    """Generates Pharmacist Notes from Evidence Pack.

    Focus areas:
    - Drug safety and risks (ADR, contraindications, DDI)
    - Monitoring and patient education
    - Taiwan availability
    """

    writer_type = "pharmacist"
    prompt_name = "pharmacist"

    @property
    def prompt_path(self) -> Path:
        """Get the path to the pharmacist prompt file."""
        return get_prompt_path("pharmacist")
