"""API endpoints for third-party integrations (Zoom, Teams, etc.)"""

import hmac
import hashlib
from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.config import settings
from app.models.meeting import Meeting

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


def verify_zoom_webhook(request_body: bytes, signature: str) -> bool:
    """Verify Zoom webhook signature"""
    if not settings.ZOOM_WEBHOOK_SECRET:
        return True  # Skip verification if secret not configured
    
    message = f"v0:{request_body.decode()}"
    hash_for_verify = hmac.new(
        settings.ZOOM_WEBHOOK_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    expected_signature = f"v0={hash_for_verify}"
    return hmac.compare_digest(signature, expected_signature)


@router.post("/zoom-webhook")
async def zoom_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_zm_signature: Optional[str] = Header(None)
):
    """
    Handle Zoom webhook events
    
    Configure this webhook in your Zoom App:
    Event types: recording.completed, recording.transcript_completed
    """
    
    body = await request.body()
    
    # Verify signature
    if x_zm_signature and not verify_zoom_webhook(body, x_zm_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    data = await request.json()
    event_type = data.get("event")
    
    if event_type == "recording.completed":
        # Handle recording completion
        payload = data.get("payload", {})
        meeting_data = payload.get("object", {})
        
        # Create meeting record
        meeting = Meeting(
            title=meeting_data.get("topic", "Zoom Meeting"),
            source_type="zoom",
            status="uploaded"
        )
        
        # Store recording URL or download file
        recording_files = meeting_data.get("recording_files", [])
        for file in recording_files:
            if file.get("file_type") in ["MP4", "M4A"]:
                # In production, download file from file.get("download_url")
                # and save to uploads directory
                pass
        
        db.add(meeting)
        await db.commit()
        
        return {"status": "received", "meeting_id": meeting.id}
    
    elif event_type == "recording.transcript_completed":
        # Handle transcript completion
        payload = data.get("payload", {})
        # Process transcript data
        pass
    
    return {"status": "received"}


@router.post("/teams-webhook")
async def teams_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Handle Microsoft Teams webhook events
    
    Configure this webhook in your Teams App
    """
    
    data = await request.json()
    
    # Handle Teams specific events
    # Implementation depends on Teams Graph API setup
    
    return {"status": "received"}


@router.post("/generic-webhook")
async def generic_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Generic webhook for custom integrations
    
    Expected payload:
    {
        "title": "Meeting Title",
        "audio_url": "https://example.com/recording.mp3",
        "transcript": "Optional transcript text",
        "metadata": {
            "participants": ["John", "Sarah"],
            "date": "2024-01-01T10:00:00Z"
        }
    }
    """
    
    data = await request.json()
    
    meeting = Meeting(
        title=data.get("title", "External Meeting"),
        source_type="webhook",
        transcript=data.get("transcript"),
        status="uploaded"
    )
    
    # Handle metadata
    metadata = data.get("metadata", {})
    if "participants" in metadata:
        meeting.participants = metadata["participants"]
    
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    # If audio URL provided, download and process
    if "audio_url" in data:
        # In production, download file and trigger processing
        pass
    
    return {
        "status": "created",
        "meeting_id": meeting.id,
        "message": "Meeting created and queued for processing"
    }
