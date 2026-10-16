# StreamLoop

## Project Overview
StreamLoop is a fully‑functional streaming‑catalog web application built **purely for educational purposes**. It showcases a **doubly circular linked list** implemented in Python and used as the **single source of truth** for the navigation carousel on the front‑end.  The project demonstrates how a classic data‑structure can power a modern‑looking UI without any database or heavy front‑end frameworks.

---

## Academic Purpose
The primary goal is to illustrate the real‑world use of a **doubly circular linked list** for bidirectional, wrap‑around navigation – a pattern often found in streaming platforms where the user can scroll infinitely forward or backward.  All navigation (next / previous) is performed on the server side, guaranteeing that the linked‑list invariants are always respected.

---

## Features
- Horizontal carousel that **loops** infinitely (tail → head, head → tail).
- Real‑time API driven navigation (`/api/next`, `/api/previous`).
- Direct selection of any title via `/api/select/<id>`.
- Search by title/description and category filtering (read‑only views).
- Detailed modal with full metadata for each piece of content.
- Reset button restores the original catalog and the initial selection.
- Validation endpoint (`/api/validate`) that checks structural invariants of the list.
- Comprehensive unit‑tests for the linked‑list logic and the Flask API.
- Dark‑theme UI with coral accent, smooth hover animations, responsive layout, and full keyboard accessibility.

---

## Technology Stack
- **Backend**: Python 3, Flask 3, plain in‑memory data structures.
- **Data Model**: `content.py` – a dataclass representing a movie or series.
- **Linked List**: `doubly_circular_linked_list.py` – generic implementation with a `current` pointer.
- **Frontend**: HTML5, vanilla JavaScript (`static/js/app.js`), vanilla CSS (`static/css/styles.css`).
- **Testing**: pytest 8.

---

## Project Structure
```
streamloop/
├── app.py                # Flask entry point & API routes
├── catalog.py            # Sample catalog creation (12 items)
├── content.py            # Content dataclass
├── doubly_circular_linked_list.py
├── __init__.py           # package marker
├── requirements.txt
├── README.md
├── tests/
│   ├── test_doubly_circular_linked_list.py
│   └── test_api.py
├── templates/
│   └── index.html        # Main UI page
└── static/
    ├── css/
    │   └── styles.css    # Dark theme with coral accent
    ├── js/
    │   └── app.js        # Front‑end logic, API calls
    └── images/
        └── placeholder.svg
```

---

## Installation
```bash
# Clone or navigate to the project folder
cd /home/abejandro/Documents/Universidad/sexto_semestre/estructuras/listas-circulares-dobles/streamloop

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Application
```bash
# Start the Flask development server
python -m streamloop.app
```
The app will be available at `http://127.0.0.1:5000/`.

---

## Running Automated Tests
```bash
pytest
```
All tests should pass (≈ 30 tests covering list operations, API endpoints and edge cases).

---

## API Documentation
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/catalog` | Returns the full catalog in forward order, the current selection and the size. |
| `GET` | `/api/current` | Returns the currently selected content item. |
| `POST` | `/api/next` | Moves the list’s current pointer to the next node and returns the new selection. |
| `POST` | `/api/previous` | Moves the pointer to the previous node and returns the new selection. |
| `POST` | `/api/select/<content_id>` | Selects the node with the given ID. |
| `GET` | `/api/content/<content_id>` | Retrieves detailed information for a single item. |
| `GET` | `/api/search?q=<query>` | Case‑insensitive search on title and description. |
| `GET` | `/api/categories` | Returns the set of all categories present in the catalog. |
| `GET` | `/api/category/<category>` | Returns items that belong to the requested category (maintains linked‑list order). |
| `POST` | `/api/reset` | Restores the original catalog and selection. |
| `GET` | `/api/health` | Simple health‑check (status, size, current ID). |
| `POST` | `/api/validate` | Runs `validate_integrity()` on the list and returns `{valid: bool, errors: []}`. |

---

## Doubly Circular Linked List Explanation
A **doubly circular linked list** is a collection of nodes where each node knows its **next** and **previous** neighbour, and the list forms a closed loop:
```
[Node A] <-> [Node B] <-> [Node C] <-> [Node D]
   ^                                   |
   |___________________________________|
```
- **Head**: reference to the first node. Its `previous` points to the **tail**.
- **Tail**: the node preceding the head (`head.previous`). Its `next` points back to the head.
- **Current pointer**: the node that the UI considers *selected*.
- **Operations**:
  - `next_item()` → `current = current.next` (O(1)).
  - `previous_item()` → `current = current.previous` (O(1)).
  - `select(id)` searches linearly (O(n)) then updates `current`.
  - `append`, `prepend`, `insert_after`, `remove` all adjust the surrounding references while preserving circularity.

Because navigation follows **real object references**, the front‑end never manipulates indices – it simply asks the server for the next or previous item.

---

## Time‑Complexity Summary
| Operation | Complexity |
|-----------|------------|
| Move to next / previous | **O(1)** (single pointer hop) |
| Access head / tail | **O(1)** |
| Search by ID | **O(n)** (linear scan) |
| Append (when tail is reachable via `head.previous`) | **O(1)** |
| Prepend | **O(1)** |
| Insert after a known node | **O(1)** (once the node is found) |
| Remove a known node | **O(1)** (once the node is found) |
| Full traversal | **O(n)** |

---

## Limitations & Design Decisions
- The catalog lives **purely in memory**; a restart clears any runtime changes.
- No database is used because the assignment focuses on the data‑structure, not persistence.
- Search and category filters create temporary Python lists for convenience – they **do not replace** the main linked list.
- Image URLs point to placeholder domains; the UI falls back to a local SVG if loading fails.
- The Flask server runs in debug mode for development; for production you would switch to a WSGI server and disable `debug=True`.

---

## Future Enhancements (optional)
- Persist the catalog to a JSON file and reload on start‑up.
- Add pagination for very large catalogs.
- Replace the static placeholder with a generated poster using an image‑generation service.
- Implement unit tests for the front‑end using a headless browser.

---

*This repository is intended for learning and demonstration. It is **not** a production‑ready streaming platform.*
