"""Pydantic schemas for meeting API"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ParticipantInfo(BaseModel):
    """Participant information"""
    name: str


class ActionItem(BaseModel):
    """Action item model"""
    description: str
    owner: Optional[str] = None
    due_date: Optional[str] = None


class Decision(BaseModel):
    """Decision model"""
    description: str


class MeetingBase(BaseModel):
    """Base meeting schema"""
    title: Optional[str] = None
    meeting_date: Optional[datetime] = None


class MeetingCreate(MeetingBase):
    """Schema for creating a meeting"""
    source_type: str = Field(..., description="upload, recording, zoom, teams")


class TranscriptUpload(BaseModel):
    """Schema for uploading transcript text"""
    transcript: str = Field(..., min_length=10)


class MeetingMinutes(BaseModel):
    """Generated meeting minutes"""
    summary: str
    duration_minutes: Optional[float] = None
    participants: List[str] = []
    key_points: List[str] = []
    decisions: List[str] = []
    action_items: List[ActionItem] = []
    next_steps: List[str] = []


class MeetingResponse(BaseModel):
    """Meeting response schema"""
    id: int
    title: Optional[str] = None
    source_type: str
    status: str
    
    # Meeting content
    transcript: Optional[str] = None
    duration_minutes: Optional[float] = None
    participants: Optional[List[str]] = None
    
    # Generated minutes
    summary: Optional[str] = None
    key_points: Optional[List[str]] = None
    decisions: Optional[List[str]] = None
    action_items: Optional[List[ActionItem]] = None
    next_steps: Optional[List[str]] = None
    
    # Metadata
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True


class MeetingListResponse(BaseModel):
    """List of meetings response"""
    meetings: List[MeetingResponse]
    total: int
