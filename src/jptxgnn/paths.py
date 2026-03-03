"""Centralized path management for the project."""

import re
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_dir() -> Path:
    """Get the data directory."""
    return get_project_root() / "data"


def get_prompts_dir() -> Path:
    """Get the prompts directory."""
    return get_project_root() / "prompts"


# Collected data directories
def get_collected_dir(source: str | None = None) -> Path:
    """Get the collected data directory.

    Args:
        source: Optional source name (clinicaltrials, pubmed, tfda, ictrp)

    Returns:
        Path to the collected data directory
    """
    base = get_data_dir() / "collected"
    if source:
        return base / source
    return base


# Bundle directories
def get_bundles_dir() -> Path:
    """Get the bundles directory."""
    return get_data_dir() / "bundles"


# Evidence Pack directories
def get_evidence_packs_dir() -> Path:
    """Get the evidence packs directory."""
    return get_data_dir() / "evidence_packs"


# Notes directories
def get_notes_dir() -> Path:
    """Get the notes directory."""
    return get_data_dir() / "notes"


def slugify(text: str) -> str:
    """Convert text to a safe filename slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified text safe for filenames
    """
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with underscores
    text = re.sub(r"[^\w\-]", "_", text)
    # Remove consecutive underscores
    text = re.sub(r"_+", "_", text)
    # Remove leading/trailing underscores
    text = text.strip("_")
    # Limit length
    return text[:50]


def get_candidate_dir(
    drug: str,
    disease: str | None = None,
    base_dir: Path | None = None,
) -> Path:
    """Get a directory for a drug-disease candidate.

    Args:
        drug: Drug name
        disease: Disease/indication name
        base_dir: Base directory (bundles, evidence_packs, or notes)

    Returns:
        Path to the candidate directory
    """
    drug_slug = slugify(drug)
    if disease:
        disease_slug = slugify(disease)
        dir_name = f"{drug_slug}_{disease_slug}"
    else:
        dir_name = drug_slug

    if base_dir is None:
        base_dir = get_bundles_dir()

    return base_dir / dir_name


def ensure_candidate_dirs(drug: str, disease: str | None = None) -> dict[str, Path]:
    """Ensure all candidate directories exist.

    Args:
        drug: Drug name
        disease: Disease/indication name

    Returns:
        Dict with paths to bundles, evidence_packs, and notes directories
    """
    dirs = {
        "bundles": get_candidate_dir(drug, disease, get_bundles_dir()),
        "evidence_packs": get_candidate_dir(drug, disease, get_evidence_packs_dir()),
        "notes": get_candidate_dir(drug, disease, get_notes_dir()),
    }

    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    return dirs
