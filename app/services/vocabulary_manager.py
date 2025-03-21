import re
import json
import random
from typing import List, Dict, Any

import aiohttp
import eng_to_ipa as ipa
from google import genai
from app.config import settings


class VocabularyManager:
    """
    Service class for handling vocabulary operations.
    Extracts new words to learn from text using Gemini API.
    """
    
    def __init__(self):
        self.dictionary_api_url = settings.dictionary_api_url
        self.dictionary_api_timeout = settings.dictionary_api_timeout
    
    async def get_vocab_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract new words to learn from text.
        
        Args:
            text: The text to extract vocabulary from
            
        Returns:
            List of vocabulary words with definitions and examples
        """
        api_key = random.choice(settings.api_keys)
        client = genai.Client(api_key=api_key)
        
        json_schema = r"""
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "word": {
        "type": "string"
      },
      "partOfSpeech": {
        "type": "string"
      },
      "definition": {
        "type": "string"
      },
      "example": {
        "type": "string"
      }
    },
    "required": ["word", "partOfSpeech", "definition", "example"]
  }
}
"""
        input_prompt = f"""
You are an expert language teacher. Your task is to identify up to 10 words from the provided text that would be valuable for a language learner to study.

Select words that are:
1. Relatively uncommon or advanced
2. Useful in various contexts
3. Worth adding to one's vocabulary

Your response must be valid JSON that strictly adheres to the JSON schema defined below, without any additional content or commentary.
{json_schema}

Return words in their singular form. Do not select more than 10 words, even if the text contains many good vocabulary candidates.

Input text: "{text}"
Output:
"""
        response = client.models.generate_content(
                    model=settings.gemini_model_name,
                    contents=[input_prompt])
        
        raw_text = response.text.strip()
        pattern = r'```json\s*(.+?)\s*```'
        match = re.search(pattern, raw_text, re.DOTALL)
        content = match.group(1).strip() if match else raw_text
        
        try:
            vocab_list = json.loads(content)
            if not isinstance(vocab_list, list):
                return []
            
            # Add phonetic information to each word
            enhanced_vocab_list = await self._add_phonetic_info(vocab_list)
            return enhanced_vocab_list
        except json.JSONDecodeError:
            return []
    
    async def _add_phonetic_info(self, vocab_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add phonetic information to each word in the vocabulary list.
        
        Args:
            vocab_list: List of vocabulary words with definitions and examples
            
        Returns:
            Enhanced list with phonetic information added
        """
        enhanced_list = []
        
        for word_entry in vocab_list:
            word = word_entry.get("word", "")
            if not word:
                enhanced_list.append(word_entry)
                continue
            
            # Initialize phonetic data
            phonetic_text = ""
            audio_url = ""
            
            # Try to get phonetic data from dictionary API
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        self.dictionary_api_url.format(word=word),
                        timeout=self.dictionary_api_timeout
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            # Extract phonetic information from API response
                            if data and isinstance(data, list):
                                first_entry = data[0]
                                # Get phonetic text from top-level phonetic field if available
                                if "phonetic" in first_entry and first_entry["phonetic"]:
                                    phonetic_text = first_entry["phonetic"]
                                
                                # Look for audio URL in phonetics array
                                if "phonetics" in first_entry and first_entry["phonetics"]:
                                    for phonetic in first_entry["phonetics"]:
                                        # Prioritize entries that have both text and audio
                                        if "audio" in phonetic and phonetic["audio"]:
                                            audio_url = phonetic["audio"]
                                            if "text" in phonetic and phonetic["text"]:
                                                phonetic_text = phonetic["text"]
                                            break
            except Exception:
                # If API request fails, continue with fallback
                pass
            
            # If no phonetic text found, use eng_to_ipa as fallback
            if not phonetic_text:
                try:
                    phonetic_text = ipa.convert(word)
                except Exception:
                    phonetic_text = ""
            
            # Add phonetic information to the word entry
            # Create new word entry with reordered keys
            new_entry = {
                "word": word_entry["word"],
                "phonetic": {
                    "text": phonetic_text,
                    "audio": audio_url
                },
                "partOfSpeech": word_entry["partOfSpeech"],
                "definition": word_entry["definition"],
                "example": word_entry["example"]
            }

            enhanced_list.append(new_entry)
        
        return enhanced_list