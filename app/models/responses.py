from typing import List, Optional
from pydantic import BaseModel

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str

class Phonetic(BaseModel):
    """Model for phonetic information."""
    text: Optional[str] = None
    audio: Optional[str] = None

class Definition(BaseModel):
    """Model for word definition."""
    definition: str
    example: Optional[str] = None
    synonyms: List[str] = []
    antonyms: List[str] = []

class Meaning(BaseModel):
    """Model for word meaning."""
    partOfSpeech: str
    definitions: List[Definition]

class DictionaryEntry(BaseModel):
    """Model for dictionary entry."""
    word: str
    phonetic: Optional[str] = None
    phonetics: List[Phonetic] = []
    origin: Optional[str] = None
    meanings: List[Meaning] 