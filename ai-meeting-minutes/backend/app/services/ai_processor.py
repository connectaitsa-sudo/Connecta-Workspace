"""AI service for generating meeting minutes from transcripts"""

import json
from openai import AsyncOpenAI
from app.core.config import settings
from app.schemas.meeting import MeetingMinutes, ActionItem
from typing import Dict, Any


class AIProcessor:
    """Service for processing transcripts with AI"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_meeting_minutes(
        self,
        transcript: str,
        custom_instructions: str = ""
    ) -> MeetingMinutes:
        """
        Generate structured meeting minutes from transcript using GPT-4
        
        Args:
            transcript: Meeting transcript text
            custom_instructions: Optional custom instructions for generation
        
        Returns:
            MeetingMinutes object with structured data
        """
        
        system_prompt = """You are an expert meeting analyst. Your task is to analyze meeting transcripts and generate comprehensive, well-structured meeting minutes.

Extract and organize the following information:
1. **Summary**: A concise 2-3 sentence overview of the meeting
2. **Duration**: Estimate the meeting duration in minutes (if mentioned or inferable)
3. **Participants**: List all unique participant names mentioned
4. **Key Discussion Points**: Main topics discussed (bullet points)
5. **Decisions Made**: Clear decisions that were agreed upon
6. **Action Items**: Specific tasks with owners and due dates
7. **Next Steps**: Follow-up actions and future plans

Return your response as a JSON object with this exact structure:
{
  "summary": "string",
  "duration_minutes": number or null,
  "participants": ["name1", "name2"],
  "key_points": ["point1", "point2"],
  "decisions": ["decision1", "decision2"],
  "action_items": [
    {
      "description": "task description",
      "owner": "person name or null",
      "due_date": "date string or null"
    }
  ],
  "next_steps": ["step1", "step2"]
}

Be thorough but concise. Focus on actionable information."""

        user_prompt = f"""Please analyze this meeting transcript and generate comprehensive meeting minutes:

TRANSCRIPT:
{transcript}

{f'ADDITIONAL INSTRUCTIONS: {custom_instructions}' if custom_instructions else ''}

Generate the meeting minutes in the specified JSON format."""

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            # Parse the response
            content = response.choices[0].message.content
            minutes_data = json.loads(content)
            
            # Convert action items to proper format
            action_items = []
            for item in minutes_data.get("action_items", []):
                action_items.append(ActionItem(**item))
            
            # Create MeetingMinutes object
            meeting_minutes = MeetingMinutes(
                summary=minutes_data.get("summary", ""),
                duration_minutes=minutes_data.get("duration_minutes"),
                participants=minutes_data.get("participants", []),
                key_points=minutes_data.get("key_points", []),
                decisions=minutes_data.get("decisions", []),
                action_items=action_items,
                next_steps=minutes_data.get("next_steps", [])
            )
            
            return meeting_minutes
            
        except Exception as e:
            raise Exception(f"AI processing failed: {str(e)}")
    
    async def extract_participants(self, transcript: str) -> list[str]:
        """Extract participant names from transcript"""
        
        prompt = """Extract all unique participant/speaker names from this meeting transcript. 
Return only a JSON array of names, e.g., ["John", "Sarah", "Mike"]

Transcript:
{transcript}"""
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt.format(transcript=transcript[:3000])}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            return data.get("participants", []) or data.get("names", [])
            
        except Exception:
            return []
    
    async def estimate_duration(self, transcript: str) -> float:
        """Estimate meeting duration from transcript"""
        # Simple estimation: ~150 words per minute speaking rate
        word_count = len(transcript.split())
        estimated_minutes = word_count / 150
        return round(estimated_minutes, 1)


# Singleton instance
ai_processor = AIProcessor()
