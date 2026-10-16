from __future__ import annotations

from .content import Content
from .doubly_circular_linked_list import DoublyCircularLinkedList


def initialize_catalog() -> DoublyCircularLinkedList:
    """Create the catalog and populate it with sample content.

    Returns
    -------
    DoublyCircularLinkedList
        The populated linked list with the initial selection set to the first item.
    """
    catalog = DoublyCircularLinkedList()
    # Sample data – 12 fictional titles across various genres.
    sample_items = [
        Content(
            id="c1",
            title="Starlight Odyssey",
            content_type="Movie",
            category="Science Fiction",
            release_year=2023,
            rating=8.2,
            duration=124,
            description="An epic journey beyond the known galaxies where a crew discovers an ancient alien civilization.",
            poster_url="https://example.com/posters/starlight_odyssey.jpg",
            featured=True,
        ),
        Content(
            id="c2",
            title="Mystic Falls",
            content_type="Series",
            category="Fantasy",
            release_year=2021,
            rating=7.9,
            duration=45,
            description="A hidden valley where mystical creatures coexist with humans, following the tale of a young wizard.",
            poster_url="https://example.com/posters/mystic_falls.jpg",
        ),
        Content(
            id="c3",
            title="The Quantum Heist",
            content_type="Movie",
            category="Action",
            release_year=2022,
            rating=8.5,
            duration=110,
            description="A team of master thieves plans a robbery that bends the laws of physics.",
            poster_url="https://example.com/posters/quantum_heist.jpg",
        ),
        Content(
            id="c4",
            title="Laughing Shadows",
            content_type="Series",
            category="Comedy",
            release_year=2020,
            rating=7.4,
            duration=30,
            description="A sitcom about a group of friends who run a paranormal investigation agency.",
            poster_url="https://example.com/posters/laughing_shadows.jpg",
        ),
        Content(
            id="c5",
            title="Chronicles of Ember",
            content_type="Movie",
            category="Adventure",
            release_year=2024,
            rating=8.1,
            duration=138,
            description="A daring explorer searches for the lost city of Ember amidst treacherous terrains.",
            poster_url="https://example.com/posters/chronicles_ember.jpg",
        ),
        Content(
            id="c6",
            title="Pixel Hearts",
            content_type="Series",
            category="Animation",
            release_year=2023,
            rating=8.3,
            duration=25,
            description="Animated series following the lives of pixelated characters in a digital world.",
            poster_url="https://example.com/posters/pixel_hearts.jpg",
        ),
        Content(
            id="c7",
            title="Silent Whispers",
            content_type="Movie",
            category="Mystery",
            release_year=2021,
            rating=7.6,
            duration=102,
            description="A detective unravels a string of silent crimes that leave no trace.",
            poster_url="https://example.com/posters/silent_whispers.jpg",
        ),
        Content(
            id="c8",
            title="Echoes of Time",
            content_type="Series",
            category="Drama",
            release_year=2022,
            rating=8.0,
            duration=50,
            description="Family drama spanning three generations, exploring love, loss, and redemption.",
            poster_url="https://example.com/posters/echoes_time.jpg",
        ),
        Content(
            id="c9",
            title="Nebula Knights",
            content_type="Movie",
            category="Science Fiction",
            release_year=2025,
            rating=8.7,
            duration=130,
            description="Space knights protect the galaxy from a rising dark force.",
            poster_url="https://example.com/posters/nebula_knights.jpg",
        ),
        Content(
            id="c10",
            title="Dreamscape",
            content_type="Series",
            category="Fantasy",
            release_year=2024,
            rating=7.8,
            duration=40,
            description="Adventurers journey through shared dreams to solve mysteries.",
            poster_url="https://example.com/posters/dreamscape.jpg",
        ),
        Content(
            id="c11",
            title="Robo Rally",
            content_type="Movie",
            category="Action",
            release_year=2023,
            rating=7.5,
            duration=115,
            description="Robots compete in a high‑speed rally across a post‑apocalyptic world.",
            poster_url="https://example.com/posters/robo_rally.jpg",
        ),
        Content(
            id="c12",
            title="Gentle Giants",
            content_type="Series",
            category="Animation",
            release_year=2022,
            rating=8.4,
            duration=22,
            description="A heart‑warming series about giant creatures living among humans.",
            poster_url="https://example.com/posters/gentle_giants.jpg",
        ),
    ]
    for item in sample_items:
        catalog.append(item)
    # Set the first item as the current selection.
    catalog.current = catalog.head
    return catalog
