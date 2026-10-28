"""In-memory storage of affiliates using a stack, a queue and a list."""

from collections import deque
from typing import Deque, List, Optional

from constants import LIST, QUEUE, STACK
from models.affiliate_data_structure import AffiliateDataStructure
from utils.formatters import format_currency


class AffiliateRepository:
    """Keeps affiliates in main memory (no files, no databases).

    * Stack : ``list``  -> append (push) / pop
    * Queue : ``deque`` -> append (enqueue) / popleft (dequeue)
    * List  : ``list``  -> append at the end / remove by ID number
    """

    def __init__(self) -> None:
        self._stack: List[AffiliateDataStructure] = []
        self._queue: Deque[AffiliateDataStructure] = deque()
        self._list: List[AffiliateDataStructure] = []

    def _get(self, structure: str):
        return {STACK: self._stack, QUEUE: self._queue, LIST: self._list}[structure]

    # -- queries ---------------------------------------------------------------
    def count(self, structure: str) -> int:
        return len(self._get(structure))

    def records(self, structure: str) -> List[AffiliateDataStructure]:
        """Records in display order (the stack shows its top first)."""
        items = list(self._get(structure))
        return items[::-1] if structure == STACK else items

    def find_by_id(self, structure: str, id_number: str) -> Optional[AffiliateDataStructure]:
        return next((a for a in self._get(structure) if a.id_number == id_number), None)

    def peek_next(self, structure: str) -> Optional[AffiliateDataStructure]:
        """Record that would leave the stack (top) or the queue (front)."""
        data = self._get(structure)
        if not data:
            return None
        return data[-1] if structure == STACK else data[0]

    # -- commands --------------------------------------------------------------
    def add(self, structure: str, affiliate: AffiliateDataStructure) -> None:
        """Push / enqueue / append at the end, depending on the structure."""
        self._get(structure).append(affiliate)

    def remove_next(self, structure: str) -> Optional[AffiliateDataStructure]:
        """Pop from the stack or dequeue from the queue."""
        if structure == STACK:
            return self._stack.pop() if self._stack else None
        if structure == QUEUE:
            return self._queue.popleft() if self._queue else None
        raise ValueError("remove_next only applies to the Stack and the Queue")

    def remove_by_id(self, id_number: str) -> Optional[AffiliateDataStructure]:
        """Remove an affiliate from the list by its ID number."""
        affiliate = self.find_by_id(LIST, id_number)
        if affiliate is not None:
            self._list.remove(affiliate)
        return affiliate

    # -- reports ---------------------------------------------------------------
    def build_report(self, structure: str) -> str:
        if structure == STACK:
            total = sum(a.affiliation_fee for a in self._stack)
            return f"Total fees: ${format_currency(total)}"
        if structure == QUEUE:
            return f"Records in queue: {len(self._queue)}"
        average = (
            sum(a.current_income for a in self._list) / len(self._list)
            if self._list
            else 0
        )
        return f"Average income: ${format_currency(average)}"
