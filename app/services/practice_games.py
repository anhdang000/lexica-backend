import json
import random
from typing import List, Dict, Any

from google import genai
from app.config import settings

class PracticeGames:
    """
    Service class for generating various vocabulary practice games and quizzes.
    """
    
    def __init__(self):
        """Initialize the PracticeGames service."""
        pass

    async def gen_quiz_sess(self, word_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate multiple choice quizzes for the given word list using Gemini API.
        
        Args:
            word_list: List of dictionaries containing word information
                      Each dict should have 'word', 'definition', and 'example' keys
            
        Returns:
            List of quiz questions, each containing:
            - word: The word being tested
            - definition: The definition of the word
            - question: The quiz question
            - options: List of 4 possible answers
            - correct_option_idx: Index of the correct answer (0-3)
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
      "definition": {
        "type": "string"
      },
      "question": {
        "type": "string"
      },
      "options": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "minItems": 4,
        "maxItems": 4
      },
      "correct_option_idx": {
        "type": "integer",
        "minimum": 0,
        "maximum": 3
      }
    },
    "required": ["word", "definition", "question", "options", "correct_option_idx"]
  }
}
"""
        # Prepare word info for the prompt
        words_info = []
        for item in word_list:
            word_info = {
                "word": item["word"],
                "definition": item["definition"],
                "example": item["example"]
            }
            words_info.append(word_info)
        
        input_prompt = f"""
You are an expert language teacher creating a vocabulary quiz. Generate multiple choice questions where students guess the word based on definitions or context. the word based on definitions or context.

For each word:
1. Create questions WITHOUT revealing the target word, question should be creative and engaging, and do not use too advanced words for the question
2. Provide 4 possible word choices, including the correct word
3. Make wrong options plausible but clearly incorrect
4. Vary question formats (definition-based, context clues, synonyms, etc.)

Words and their information:
{json.dumps(words_info, indent=2)}

Return a JSON array strictly following this schema, with no additional text:
{json_schema}

Make sure:
- Each question has exactly 4 options
- correct_option_idx is 0-3, indicating which option is correct
- Questions should NOT contain the target worde target word
- Questions should test word recognition from definitions/context
- Wrong answers should be plausible words in similar category
    """

        response = client.models.generate_content(
            model=settings.gemini_model_name,
            contents=[input_prompt]
        )

        raw_text = response.text.strip()
        try:
            # Try to extract JSON if it's wrapped in code blocks
            if raw_text.startswith('```') and raw_text.endswith('```'):
                content = raw_text.split('```')[1]
                if content.startswith('json'):
                    content = content[4:].strip()
            else:
                content = raw_text
            
            quiz_data = json.loads(content)
            
            # Validate the structure
            if not isinstance(quiz_data, list):
                return []
            
            for quiz in quiz_data:
                if not all(key in quiz for key in ['word', 'definition', 'question', 'options', 'correct_option_idx']):
                    return []
                if len(quiz['options']) != 4:
                    return []
                if not 0 <= quiz['correct_option_idx'] <= 3:
                    return []
            
            return quiz_data
            
        except json.JSONDecodeError:
            return []