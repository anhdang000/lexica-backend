import re
from typing import Optional

# Keep clean_text and validate_word functions as they are
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


def preprocess_markdown(text: str) -> str:
    """
    Preprocess markdown text:
    1. Remove all href parts with format: [something](link) COMPLETELY
    2. Remove standalone or malformed URLs (http://, https://, www., httpswww...)
    3. Remove excess blank spaces
    4. Remove 2 or more consecutive special characters and spaces

    Args:
        text: The markdown text to process

    Returns:
        Processed text with cleaner format
    """
    if not isinstance(text, str):
        return ""

    # 1. Remove standard Markdown links COMPLETELY: [text](url) -> (nothing)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', '', text)

    # 2. Remove standalone URLs (including common malformations like missing // or starting with www)
    #    Regex explanation:
    #    \b            - Word boundary, ensures we don't match mid-word
    #    (https?://? - Matches 'http://', 'https://', 'http', 'https' (optional //)
    #    |www\.       - OR matches 'www.' literally
    #    )             - End of group
    #    [^\s()<>]+    - Matches one or more characters that are NOT whitespace or common wrapping brackets
    #    (?:\([^\s()<>]*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])* - Optionally matches balanced parentheses or trailing punctuation
    #    This more complex regex attempts to handle URLs more robustly, including those followed by punctuation.
    #    A simpler version could be: r'\b(https?://?|www\.)[^\s]+'
    url_pattern = r'\b(https?://?|www\.)[^\s()<>]+(?:\([^\s()<>]*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])*'
    text = re.sub(url_pattern, '', text)

    # 3. Remove excess blank spaces (leading, trailing, and multiple spaces)
    #    Run this *after* removals to clean up leftover spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # 4. Handle specific cases / special character cleanup
    #    Temporarily replace percentages
    text = re.sub(r'(\d+)%', r'\1percent', text)

    #    Remove 2+ consecutive non-alphanumeric characters (excluding space)
    #    This helps clean up things like '))' left after URL removal
    text = re.sub(r'[^\w\s]{2,}', '', text) # \w includes letters, numbers, underscore

    #    Remove isolated single non-word, non-space characters
    #    This helps clean up single punctuation like ')' if isolated by spaces
    text = re.sub(r'(?<!\w)[^\w\s](?!\w)', '', text)

    #    Restore percentages
    text = re.sub(r'(\d+)percent', r'\1%', text)

    #    Handle spaces between letters and numbers (Optional - often too aggressive)
    #    text = re.sub(r'([a-zA-Z])\s+(\d+)', r'\1\2', text)

    # 5. Final cleanup of spaces that might have been introduced or left over
    text = re.sub(r'\s+', ' ', text).strip()

    return text