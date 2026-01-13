"""Multilingual support for AI Meeting Minutes System"""

from typing import Dict, Any
from openai import AsyncOpenAI
from app.core.config import settings

class MultilingualService:
    """Service for multilingual transcription and translation"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Supported languages
        self.supported_languages = {
            'en': 'English',
            'ar': 'Arabic',
            'ur': 'Urdu',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'zh': 'Chinese',
            'ja': 'Japanese'
        }
    
    async def transcribe_with_language_detection(
        self,
        audio_file_path: str
    ) -> Dict[str, Any]:
        """
        Transcribe audio with automatic language detection
        Supports Arabic, Urdu, Hindi, English, and many more
        """
        with open(audio_file_path, "rb") as audio_file:
            transcript_response = await self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json"
            )
        
        return {
            "text": transcript_response.text,
            "language": transcript_response.language,
            "duration": getattr(transcript_response, "duration", None)
        }
    
    async def generate_bilingual_minutes(
        self,
        transcript: str,
        primary_language: str = "en",
        secondary_language: str = "ar"
    ) -> Dict[str, Any]:
        """
        Generate meeting minutes in two languages
        Primary: English, Secondary: Arabic (or any combination)
        """
        
        system_prompt = f"""You are an expert multilingual meeting analyst. 
Generate comprehensive meeting minutes in BOTH {self.supported_languages.get(primary_language, 'English')} 
and {self.supported_languages.get(secondary_language, 'Arabic')}.

Extract and organize the following information in BOTH languages:
1. Summary (2-3 sentences)
2. Duration (estimate in minutes)
3. Participants (list of names)
4. Key Discussion Points (bullet points)
5. Decisions Made (clear decisions)
6. Action Items (with owners and due dates)
7. Next Steps (follow-up actions)

Return your response as a JSON object with this structure:
{{
  "{primary_language}": {{
    "summary": "string",
    "duration_minutes": number,
    "participants": ["name1", "name2"],
    "key_points": ["point1", "point2"],
    "decisions": ["decision1", "decision2"],
    "action_items": [
      {{"description": "task", "owner": "person", "due_date": "date"}}
    ],
    "next_steps": ["step1", "step2"]
  }},
  "{secondary_language}": {{
    "summary": "string in {self.supported_languages.get(secondary_language, 'Arabic')}",
    "duration_minutes": number,
    "participants": ["name1", "name2"],
    "key_points": ["point1 in {self.supported_languages.get(secondary_language, 'Arabic')}", "point2"],
    "decisions": ["decision1 in {self.supported_languages.get(secondary_language, 'Arabic')}", "decision2"],
    "action_items": [
      {{"description": "task in {self.supported_languages.get(secondary_language, 'Arabic')}", "owner": "person", "due_date": "date"}}
    ],
    "next_steps": ["step1 in {self.supported_languages.get(secondary_language, 'Arabic')}", "step2"]
  }}
}}

Be thorough but concise. Ensure translations are accurate and culturally appropriate."""

        user_prompt = f"""Please analyze this meeting transcript and generate comprehensive meeting minutes in BOTH {self.supported_languages.get(primary_language, 'English')} and {self.supported_languages.get(secondary_language, 'Arabic')}:

TRANSCRIPT:
{transcript}

Generate the bilingual meeting minutes in the specified JSON format."""

        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        minutes_data = json.loads(response.choices[0].message.content)
        
        return minutes_data
    
    async def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str
    ) -> str:
        """
        Translate text from one language to another
        Supports: English, Arabic, Urdu, Hindi, and more
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a professional translator. Translate the following text from {self.supported_languages.get(source_language, source_language)} to {self.supported_languages.get(target_language, target_language)}. Maintain the original meaning, tone, and format."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text
        Returns ISO language code
        """
        # Simple detection based on character sets
        import re
        
        # Arabic script
        if re.search(r'[\u0600-\u06FF]', text):
            return 'ar'
        
        # Urdu (uses Arabic script with additional characters)
        if re.search(r'[\u0600-\u06FF\u0750-\u077F]', text):
            return 'ur'
        
        # Hindi (Devanagari script)
        if re.search(r'[\u0900-\u097F]', text):
            return 'hi'
        
        # Default to English
        return 'en'


# Singleton instance
multilingual_service = MultilingualService()
