import hashlib
import structlog

logger = structlog.get_logger(__name__)


class Deduplicator:
    """
    Tracks article hashes in memory to detect duplicates
    during a single ingestion run.
    """

    def __init__(self):
        self._seen: set[str] = set()

    def is_duplicate(self, text: str) -> bool:
        h = self._hash(text)
        if h in self._seen:
            logger.warning("Duplicate article detected, skipping")
            return True
        self._seen.add(h)
        return False

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @property
    def seen_count(self) -> int:
        return len(self._seen)