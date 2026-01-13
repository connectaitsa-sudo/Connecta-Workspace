"""API endpoints for meeting management"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.meeting import Meeting
from app.schemas.meeting import (
    MeetingResponse,
    MeetingListResponse,
    TranscriptUpload,
    MeetingMinutes
)
from app.services.transcription import transcription_service
from app.services.ai_processor import ai_processor
from app.services.export_service import export_service

router = APIRouter(prefix="/api/meetings", tags=["meetings"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


async def process_meeting_background(meeting_id: int, db: AsyncSession):
    """Background task to process meeting (transcribe + generate minutes)"""
    try:
        # Get meeting from database
        result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
        meeting = result.scalar_one_or_none()
        
        if not meeting:
            return
        
        # Update status to transcribing
        meeting.status = "transcribing"
        await db.commit()
        
        # Transcribe audio if audio file exists
        if meeting.audio_file_path and os.path.exists(meeting.audio_file_path):
            transcript_data = await transcription_service.transcribe_audio(meeting.audio_file_path)
            meeting.transcript = transcript_data["text"]
            meeting.transcript_raw = transcript_data
        
        # Update status to processing
        meeting.status = "processing"
        await db.commit()
        
        # Generate meeting minutes with AI
        if meeting.transcript:
            minutes = await ai_processor.generate_meeting_minutes(meeting.transcript)
            
            # Update meeting with generated content
            meeting.summary = minutes.summary
            meeting.duration_minutes = minutes.duration_minutes
            meeting.participants = minutes.participants
            meeting.key_points = minutes.key_points
            meeting.decisions = minutes.decisions
            meeting.action_items = [item.dict() for item in minutes.action_items]
            meeting.next_steps = minutes.next_steps
        
        # Mark as completed
        meeting.status = "completed"
        await db.commit()
        
    except Exception as e:
        # Update meeting with error
        meeting.status = "failed"
        meeting.error_message = str(e)
        await db.commit()


@router.post("/upload-audio", response_model=MeetingResponse)
async def upload_audio_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """Upload audio/video file for transcription and analysis"""
    
    # Validate file type
    allowed_extensions = ['.mp3', '.mp4', '.wav', '.m4a', '.webm', '.ogg', '.flac']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Create meeting record
    meeting = Meeting(
        title=title or file.filename,
        source_type="upload",
        status="uploaded"
    )
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    # Save uploaded file
    file_path = os.path.join(settings.UPLOAD_DIR, f"meeting_{meeting.id}{file_ext}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        meeting.audio_file_path = file_path
        await db.commit()
        
        # Process in background
        background_tasks.add_task(process_meeting_background, meeting.id, db)
        
        return meeting
        
    except Exception as e:
        meeting.status = "failed"
        meeting.error_message = str(e)
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


@router.post("/upload-transcript", response_model=MeetingResponse)
async def upload_transcript_text(
    background_tasks: BackgroundTasks,
    data: TranscriptUpload,
    title: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Upload meeting transcript text directly for analysis"""
    
    # Create meeting record
    meeting = Meeting(
        title=title or "Transcript Upload",
        source_type="transcript",
        transcript=data.transcript,
        status="transcribed"
    )
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    # Process in background (generate minutes only)
    async def process_transcript_background(meeting_id: int):
        try:
            result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
            meeting_obj = result.scalar_one_or_none()
            
            if meeting_obj and meeting_obj.transcript:
                meeting_obj.status = "processing"
                await db.commit()
                
                minutes = await ai_processor.generate_meeting_minutes(meeting_obj.transcript)
                
                meeting_obj.summary = minutes.summary
                meeting_obj.duration_minutes = minutes.duration_minutes
                meeting_obj.participants = minutes.participants
                meeting_obj.key_points = minutes.key_points
                meeting_obj.decisions = minutes.decisions
                meeting_obj.action_items = [item.dict() for item in minutes.action_items]
                meeting_obj.next_steps = minutes.next_steps
                meeting_obj.status = "completed"
                await db.commit()
        except Exception as e:
            meeting_obj.status = "failed"
            meeting_obj.error_message = str(e)
            await db.commit()
    
    background_tasks.add_task(process_transcript_background, meeting.id)
    
    return meeting


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get meeting details by ID"""
    
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return meeting


@router.get("/", response_model=MeetingListResponse)
async def list_meetings(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """List all meetings"""
    
    # Get total count
    count_result = await db.execute(select(Meeting))
    total = len(count_result.scalars().all())
    
    # Get meetings with pagination
    result = await db.execute(
        select(Meeting)
        .order_by(Meeting.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    meetings = result.scalars().all()
    
    return MeetingListResponse(meetings=meetings, total=total)


@router.delete("/{meeting_id}")
async def delete_meeting(
    meeting_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a meeting"""
    
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Delete associated files
    if meeting.audio_file_path and os.path.exists(meeting.audio_file_path):
        os.remove(meeting.audio_file_path)
    
    await db.delete(meeting)
    await db.commit()
    
    return {"message": "Meeting deleted successfully"}


@router.get("/{meeting_id}/export/{format}")
async def export_meeting(
    meeting_id: int,
    format: str,
    db: AsyncSession = Depends(get_db)
):
    """Export meeting minutes in specified format (pdf, docx, txt)"""
    
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if meeting.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Meeting processing not completed yet"
        )
    
    # Create MeetingMinutes object
    from app.schemas.meeting import ActionItem
    
    action_items = []
    if meeting.action_items:
        for item in meeting.action_items:
            action_items.append(ActionItem(**item))
    
    minutes = MeetingMinutes(
        summary=meeting.summary or "",
        duration_minutes=meeting.duration_minutes,
        participants=meeting.participants or [],
        key_points=meeting.key_points or [],
        decisions=meeting.decisions or [],
        action_items=action_items,
        next_steps=meeting.next_steps or []
    )
    
    # Export to requested format
    format_lower = format.lower()
    title = meeting.title or f"Meeting {meeting.id}"
    
    if format_lower == "pdf":
        filepath = export_service.export_to_pdf(meeting.id, minutes, title)
    elif format_lower == "docx":
        filepath = export_service.export_to_docx(meeting.id, minutes, title)
    elif format_lower == "txt":
        filepath = export_service.export_to_txt(meeting.id, minutes, title)
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid format. Supported: pdf, docx, txt"
        )
    
    # Return file
    return FileResponse(
        path=filepath,
        filename=os.path.basename(filepath),
        media_type="application/octet-stream"
    )


@router.post("/{meeting_id}/regenerate", response_model=MeetingResponse)
async def regenerate_minutes(
    meeting_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Regenerate meeting minutes from existing transcript"""
    
    result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
    meeting = result.scalar_one_or_none()
    
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    if not meeting.transcript:
        raise HTTPException(
            status_code=400,
            detail="No transcript available for this meeting"
        )
    
    # Process in background
    async def regenerate_background(meeting_id: int):
        try:
            result = await db.execute(select(Meeting).where(Meeting.id == meeting_id))
            meeting_obj = result.scalar_one_or_none()
            
            if meeting_obj:
                meeting_obj.status = "processing"
                await db.commit()
                
                minutes = await ai_processor.generate_meeting_minutes(meeting_obj.transcript)
                
                meeting_obj.summary = minutes.summary
                meeting_obj.duration_minutes = minutes.duration_minutes
                meeting_obj.participants = minutes.participants
                meeting_obj.key_points = minutes.key_points
                meeting_obj.decisions = minutes.decisions
                meeting_obj.action_items = [item.dict() for item in minutes.action_items]
                meeting_obj.next_steps = minutes.next_steps
                meeting_obj.status = "completed"
                await db.commit()
        except Exception as e:
            meeting_obj.status = "failed"
            meeting_obj.error_message = str(e)
            await db.commit()
    
    background_tasks.add_task(regenerate_background, meeting.id)
    meeting.status = "processing"
    await db.commit()
    
    return meeting
