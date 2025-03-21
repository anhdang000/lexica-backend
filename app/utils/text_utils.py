import re
from typing import Optional

def clean_text(text: str) -> str:
    """
    Clean and normalize the input text.
    
    Args:
        text: The input text to clean
        
    Returns:
        Cleaned text with only alphanumeric characters and spaces
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
        
    # Remove special characters and normalize spaces
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def validate_word(word: str) -> Optional[str]:
    """
    Validate and clean a word for dictionary lookup.
    
    Args:
        word: The word to validate
        
    Returns:
        Cleaned word if valid, None if invalid
    """
    cleaned_word = clean_text(word)
    return cleaned_word if cleaned_word else None 