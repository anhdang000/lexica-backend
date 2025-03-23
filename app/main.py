from fastapi import FastAPI, HTTPException, Query, Body
from app.models.responses import HealthResponse, DictionaryEntry
from app.services.dictionary import Dictionary
from app.services.vocabulary_manager import VocabularyManager
from app.services.practice_games import PracticeGames
from app.utils.text_utils import validate_word
from typing import List, Dict, Any

app = FastAPI(
    title="Dictionary Lookup API",
    description="A simple API for looking up word definitions",
    version="1.0.0"
)

# Initialize services
dictionary = Dictionary()
vocabulary_manager = VocabularyManager()
practice_games = PracticeGames()

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}

@app.get("/lookup/{word}", tags=["Dictionary"])
async def lookup_word(word: str):
    """
    Look up a word in the dictionary and optionally translate to target language.
    
    Args:
        word: The word to look up
        
    Returns:
        Dictionary entries for the requested word
    """
    # Validate and clean the input word
    cleaned_word = validate_word(word)

    if not cleaned_word:
        raise HTTPException(
            status_code=400,
            detail="Invalid word provided"
        )
    
    # Look up the word using the dictionary service
    return await dictionary.lookup_word_base_en(cleaned_word)


@app.post("/vocab/extract_text", tags=["Vocabulary"])
async def get_vocab_text(text: str = Body(..., description="Text to extract vocabulary from")):
    """
    Extract vocabulary words from provided text.
    
    Args:
        text: The text to analyze for vocabulary extraction
        
    Returns:
        List of vocabulary words with definitions, examples, and difficulty levels
    """
    if not text or len(text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Text is too short or empty"
        )
    
    # Extract vocabulary from text using the vocabulary manager service
    return await vocabulary_manager.get_vocab_text(text)

@app.post("/practice/quiz", tags=["Practice"])
async def generate_quiz(word_list: List[Dict[str, Any]] = Body(..., description="List of words with their information to generate quiz from")):
    """
    Generate a quiz session from a list of words.
    
    Args:
        word_list: List of dictionaries containing word information
                  Each dict should have 'word', 'definition', and 'example' keys
        
    Returns:
        List of quiz questions with multiple choice options
    """
    if not word_list or len(word_list) == 0:
        raise HTTPException(
            status_code=400,
            detail="Word list is empty"
        )
    
    # Validate each word entry has required fields
    required_fields = {'word', 'definition', 'example'}
    for entry in word_list:
        if not all(field in entry for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail="Each word entry must contain word, definition, and example"
            )
    
    # Generate quiz using practice games service
    return await practice_games.gen_quiz_sess(word_list)

