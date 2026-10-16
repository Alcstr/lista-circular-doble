"""Doubly Circular Linked List implementation for StreamLoop.

This module provides a generic doubly circular linked list with a current pointer.
It is used as the source of truth for the navigation carousel in the StreamLoop
application.

The implementation follows the invariants described in the project specification:
1. The list is circular: head.previous points to tail, tail.next points to head.
2. Each node's next.previous and previous.next reference the node itself.
3. Traversal using next or previous eventually returns to the head.
4. No node in a non‑empty list has a null next or previous reference.
"""

from __future__ import annotations
from typing import Any, Optional, List


class Node:
    """A node in the doubly circular linked list.

    Attributes
    ----------
    data: Any
        The payload stored in the node (in StreamLoop this will be a Content
        instance).
    next: Node
        Reference to the next node in the list.
    previous: Node
        Reference to the previous node in the list.
    """

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[Node] = None
        self.previous: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(id={getattr(self.data, 'id', None)!r})"


class DoublyCircularLinkedList:
    """A reusable doubly circular linked list.

    The list maintains a reference to the *head* node, a *size* counter and a
    *current* node which represents the selected item in the UI.
    """

    def __init__(self):
        self.head: Optional[Node] = None
        self.size: int = 0
        self.current: Optional[Node] = None

    # ---------------------------------------------------------------------
    # Core mutation helpers
    # ---------------------------------------------------------------------
    def _link_nodes(self, node_a: Node, node_b: Node) -> None:
        """Link ``node_a`` -> ``node_b`` in forward direction.
        ``node_a.next`` becomes ``node_b`` and ``node_b.previous`` becomes
        ``node_a``.
        """
        node_a.next = node_b
        node_b.previous = node_a

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def append(self, data: Any) -> Node:
        """Append ``data`` to the tail of the list.

        Returns
        -------
        Node
            The newly created node.
        """
        new_node = Node(data)
        if self.head is None:
            # First node – points to itself in both directions.
            new_node.next = new_node.previous = new_node
            self.head = self.current = new_node
        else:
            tail = self.head.previous  # type: ignore[arg-type]
            # Insert new_node after tail.
            self._link_nodes(tail, new_node)
            self._link_nodes(new_node, self.head)
        self.size += 1
        return new_node

    def prepend(self, data: Any) -> Node:
        """Insert ``data`` before the current head and make it the new head.
        """
        new_node = Node(data)
        if self.head is None:
            new_node.next = new_node.previous = new_node
            self.head = self.current = new_node
        else:
            tail = self.head.previous  # type: ignore[arg-type]
            # Link tail <-> new_node <-> current head
            self._link_nodes(tail, new_node)
            self._link_nodes(new_node, self.head)
            self.head = new_node
        self.size += 1
        return new_node

    def insert_after(self, target_id: Any, data: Any) -> Optional[Node]:
        """Insert ``data`` after the node whose ``data.id`` matches ``target_id``.

        Returns the created node or ``None`` if the target is not found.
        """
        target = self.find(target_id)
        if target is None:
            return None
        new_node = Node(data)
        successor = target.next  # type: ignore[arg-type]
        self._link_nodes(target, new_node)
        self._link_nodes(new_node, successor)
        self.size += 1
        return new_node

    def remove(self, target_id: Any) -> bool:
        """Remove the node with ``data.id == target_id``.

        Returns ``True`` if removal succeeded, ``False`` otherwise.
        """
        if self.head is None:
            return False
        node = self.find(target_id)
        if node is None:
            return False
        # Update current pointer safely.
        if self.current is node:
            self.current = node.next if self.size > 1 else None
        if self.size == 1:
            # Removing the only node.
            self.head = None
            self.current = None
        else:
            # Relink neighbors.
            prev_node = node.previous  # type: ignore[arg-type]
            next_node = node.next  # type: ignore[arg-type]
            self._link_nodes(prev_node, next_node)
            # If we removed the head, move head reference.
            if node is self.head:
                self.head = next_node
        self.size -= 1
        return True

    def find(self, target_id: Any) -> Optional[Node]:
        """Return the node whose ``data.id`` equals ``target_id``.
        Linear search – O(n).
        """
        if self.head is None:
            return None
        node = self.head
        for _ in range(self.size):
            if getattr(node.data, "id", None) == target_id:
                return node
            node = node.next  # type: ignore[assignment]
        return None

    def get_head(self) -> Optional[Node]:
        return self.head

    def get_tail(self) -> Optional[Node]:
        if self.head is None:
            return None
        return self.head.previous  # type: ignore[arg-type]

    def select(self, target_id: Any) -> Optional[Any]:
        """Select the node with ``target_id`` as the current node.
        Returns the payload data or ``None`` if not found.
        """
        node = self.find(target_id)
        if node:
            self.current = node
            return node.data
        return None

    def get_current(self) -> Optional[Any]:
        return self.current.data if self.current else None

    def next_item(self) -> Optional[Any]:
        """Advance the current pointer to the next node and return its data.
        """
        if self.current:
            self.current = self.current.next  # type: ignore[assignment]
            return self.current.data
        return None

    def previous_item(self) -> Optional[Any]:
        """Move the current pointer to the previous node and return its data.
        """
        if self.current:
            self.current = self.current.previous  # type: ignore[assignment]
            return self.current.data
        return None

    def traverse_forward(self) -> List[Any]:
        """Return a list of payloads traversing from head forward.
        """
        items: List[Any] = []
        if self.head is None:
            return items
        node = self.head
        for _ in range(self.size):
            items.append(node.data)
            node = node.next  # type: ignore[assignment]
        return items

    def traverse_backward(self) -> List[Any]:
        """Return a list of payloads traversing from tail backward.
        """
        items: List[Any] = []
        if self.head is None:
            return items
        node = self.get_tail()
        for _ in range(self.size):
            items.append(node.data)  # type: ignore[arg-type]
            node = node.previous  # type: ignore[assignment]
        return items

    def to_list(self) -> List[Any]:
        """Alias for ``traverse_forward`` – returns items in logical order.
        """
        return self.traverse_forward()

    # ---------------------------------------------------------------------
    # Validation
    # ---------------------------------------------------------------------
    def validate_integrity(self) -> dict:
        """Validate structural invariants.

        Returns a dictionary with ``valid`` (bool) and ``errors`` (list of strings).
        """
        errors: List[str] = []
        if self.head is None:
            if self.size != 0:
                errors.append("Empty list should have size 0.")
            if self.current is not None:
                errors.append("Empty list should have no current node.")
            return {"valid": len(errors) == 0, "errors": errors}
        # Non‑empty list checks
        if self.size < 1:
            errors.append("Non‑empty list must have size >= 1.")
        # Verify circular connections.
        tail = self.head.previous  # type: ignore[arg-type]
        if tail.next is not self.head:
            errors.append("Tail's next does not point to head.")
        if self.head.previous is not tail:
            errors.append("Head's previous does not point to tail.")
        # Walk forward verifying each node's back‑reference.
        node = self.head
        for i in range(self.size):
            if node.next is None or node.previous is None:
                errors.append(f"Node {i} has null next/previous.")
                break
            if node.next.previous is not node:
                errors.append(f"node.next.previous mismatch at node {i}.")
            if node.previous.next is not node:
                errors.append(f"node.previous.next mismatch at node {i}.")
            node = node.next  # type: ignore[assignment]
        # Verify that we end back at head.
        if node is not self.head:
            errors.append("Forward traversal did not return to head.")
        # Verify current pointer is in the list (if set).
        if self.current:
            found = False
            node = self.head
            for _ in range(self.size):
                if node is self.current:
                    found = True
                    break
                node = node.next  # type: ignore[assignment]
            if not found:
                errors.append("Current pointer is not a member of the list.")
        return {"valid": len(errors) == 0, "errors": errors}

    # ---------------------------------------------------------------------
    # Utility helpers for debugging / representation
    # ---------------------------------------------------------------------
    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return f"DoublyCircularLinkedList(size={self.size})"
