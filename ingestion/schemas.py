from pydantic import BaseModel, field_validator
from typing import Optional


class RawArticle(BaseModel):
    id: str
    article: str
    highlights: str


class CleanedArticle(BaseModel):
    id: str
    article: str
    highlights: str
    word_count: int
    char_count: int
    is_valid: bool = True

    @field_validator("article")
    @classmethod
    def article_must_not_be_empty(cls, v):
        if not v or len(v.strip()) < 50:
            raise ValueError("Article too short to be useful")
        return v