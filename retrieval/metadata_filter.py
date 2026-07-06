from dataclasses import dataclass, field


@dataclass
class MetadataFilter:
    """
    Structured way to build Qdrant-compatible filters.
    Keeps filter logic out of retriever code.
    """
    must: dict = field(default_factory=dict)

    def add(self, field_name: str, value) -> "MetadataFilter":
        self.must[field_name] = value
        return self

    def to_dict(self) -> dict:
        return self.must.copy()

    def is_empty(self) -> bool:
        return len(self.must) == 0