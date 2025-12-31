"""Database models for meetings"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from datetime import datetime
from app.core.database import Base


class Meeting(Base):
    """Meeting model"""
    
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    
    # Meeting source
    source_type = Column(String(50))  # upload, recording, zoom, teams
    audio_file_path = Column(String(500), nullable=True)
    video_file_path = Column(String(500), nullable=True)
    
    # Transcription
    transcript = Column(Text, nullable=True)
    transcript_raw = Column(JSON, nullable=True)  # Raw response from transcription service
    
    # Meeting metadata
    duration_minutes = Column(Float, nullable=True)
    participants = Column(JSON, nullable=True)  # List of participant names
    meeting_date = Column(DateTime, nullable=True)
    
    # Generated content
    summary = Column(Text, nullable=True)
    key_points = Column(JSON, nullable=True)  # List of key discussion points
    decisions = Column(JSON, nullable=True)  # List of decisions made
    action_items = Column(JSON, nullable=True)  # List of action items
    next_steps = Column(JSON, nullable=True)  # List of next steps
    
    # Status
    status = Column(String(50), default="uploaded")  # uploaded, transcribing, transcribed, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Export tracking
    exported_formats = Column(JSON, nullable=True)  # List of exported formats (pdf, docx, etc.)
