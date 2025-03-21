import re
import json
import random

import requests
import aiohttp
import eng_to_ipa as ipa
from typing import Dict, List, Any, Optional
from fastapi import HTTPException
from google import genai
from google.genai import types

from app.config import settings



class Dictionary:
    """Service class for handling dictionary operations."""
    
    def __init__(self):
        self.api_url = settings.dictionary_api_url
        self.timeout = settings.dictionary_api_timeout
        self.max_retries = settings.dictionary_api_max_retries
    
    async def lookup_word_base_en(self, word: str) -> List[Dict[str, Any]] | None:
        """
        Look up a word in the dictionary asynchronously.
        
        Args:
            word: The word to look up
            
        Returns:
            List of dictionary entries for the word in simplified format or None if not found
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url.format(word=word),
                    timeout=self.timeout
                ) as response:
                    if response.status != 200:
                        return None
                    
                    data = await response.json()
                    
                    # Transform the response to the required format
                    result = []
                    for entry in data:
                        transformed_entry = {
                            "word": entry.get("word", word),
                            "phonetic": {},
                            "meanings": []
                        }
                        
                        # Handle phonetics
                        phonetic_text = None
                        audio_url = None
                        
                        # Try to get phonetic text from the API response
                        if "phonetics" in entry and entry["phonetics"]:
                            for phonetic in entry["phonetics"]:
                                if "text" in phonetic and phonetic["text"]:
                                    phonetic_text = phonetic["text"]
                                    if "audio" in phonetic and phonetic["audio"]:
                                        audio_url = phonetic["audio"]
                                    break
                        
                        # If no phonetic text found, use eng_to_ipa as fallback
                        if not phonetic_text:
                            try:
                                phonetic_text = ipa.convert(word)
                            except Exception:
                                phonetic_text = ""
                        
                        transformed_entry["phonetic"] = {
                            "text": phonetic_text,
                            "audio": audio_url or ""
                        }
                        
                        # Handle meanings
                        if "meanings" in entry:
                            for meaning in entry["meanings"]:
                                transformed_meaning = {
                                    "partOfSpeech": meaning.get("partOfSpeech", ""),
                                    "definitions": []
                                }
                                
                                if "definitions" in meaning:
                                    for definition in meaning["definitions"]:
                                        transformed_definition = {
                                            "definition": definition.get("definition", ""),
                                            "example": definition.get("example", "")
                                        }
                                        transformed_meaning["definitions"].append(transformed_definition)
                                
                                transformed_entry["meanings"].append(transformed_meaning)
                        
                        result.append(transformed_entry)
                    
                    return result
        
        except aiohttp.ClientError:
            return None
        except Exception:
            return None
        
    async def lookup_word(self, word: str, target_lang: str) -> List[Dict[str, Any]]:
        """
        Look up a word in the dictionary and optionally translate to target language.
        
        Args:
            word: The word to look up
            target_lang: Target language code (default: "en" for English)
            
        Returns:
            Dictionary entries for the requested word in the target language
        """
        # For now, we'll just return the English definition
        # In the future, this could be expanded to support translations
        result = await self.lookup_word_base_en(word)
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Word '{word}' not found in dictionary"
            )
        return result