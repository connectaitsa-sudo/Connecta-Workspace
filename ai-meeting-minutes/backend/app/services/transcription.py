"""Audio transcription service using OpenAI Whisper"""

import os
from openai import AsyncOpenAI
from app.core.config import settings
from typing import Optional


class TranscriptionService:
    """Service for transcribing audio files"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def transcribe_audio(
        self,
        audio_file_path: str,
        language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio file using OpenAI Whisper
        
        Args:
            audio_file_path: Path to audio file
            language: Optional language code (e.g., 'en', 'es')
        
        Returns:
            dict with 'text' and optional 'segments' for timestamps
        """
        
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        try:
            with open(audio_file_path, "rb") as audio_file:
                # Transcribe using Whisper API
                transcript_response = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    language=language
                )
            
            # Extract transcript data
            result = {
                "text": transcript_response.text,
                "language": getattr(transcript_response, "language", None),
                "duration": getattr(transcript_response, "duration", None),
                "segments": getattr(transcript_response, "segments", None)
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    async def transcribe_with_speaker_detection(
        self,
        audio_file_path: str
    ) -> dict:
        """
        Transcribe with speaker diarization (requires AssemblyAI or similar service)
        This is a placeholder - implement with AssemblyAI if needed
        """
        # For now, use basic transcription
        return await self.transcribe_audio(audio_file_path)


# Singleton instance
transcription_service = TranscriptionService()
