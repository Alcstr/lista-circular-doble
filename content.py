"""Content model for StreamLoop.

Defines the data structure representing a movie or series entry.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class Content:
    id: str
    title: str
    content_type: str  # "Movie" or "Series"
    category: str
    release_year: int
    rating: float
    duration: int  # minutes
    description: str
    poster_url: str
    featured: bool = False

    def to_dict(self) -> Dict:
        """Serialize the content to a plain dict for JSON responses."""
        # asdict will include all fields.
        return asdict(self)
