"""API endpoints for third-party integrations (Zoom, Teams, etc.)"""

import os
import secrets
from fastapi import APIRouter, Request, Depends, HTTPException, Header, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.core.config import settings
from app.models.meeting import Meeting
from app.services.zoom_service import zoom_service
from app.services.teams_service import teams_service

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


# ==================== ZOOM INTEGRATION ====================

@router.get("/zoom/auth")
async def zoom_auth():
    """Initiate Zoom OAuth flow"""
    state = secrets.token_urlsafe(32)
    redirect_uri = "http://localhost:8000/api/integrations/zoom/callback"
    
    auth_url = zoom_service.get_authorization_url(redirect_uri, state)
    return {"authorization_url": auth_url, "state": state}


@router.get("/zoom/callback")
async def zoom_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Handle Zoom OAuth callback"""
    try:
        redirect_uri = "http://localhost:8000/api/integrations/zoom/callback"
        
        # Exchange code for tokens
        token_data = await zoom_service.exchange_code_for_token(code, redirect_uri)
        
        # Get user info
        user_info = await zoom_service.get_user_info(token_data["access_token"])
        
        # Store tokens in database (you should create a UserIntegration model for this)
        # For now, just return success
        
        # Redirect to frontend with success
        html_content = """
        <html>
        <head><title>Zoom Connected!</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #4285F4;">✓ Zoom Connected Successfully!</h1>
            <p>You can close this window now.</p>
            <script>
                setTimeout(() => window.close(), 2000);
            </script>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
    
    except Exception as e:
        html_content = f"""
        <html>
        <head><title>Connection Failed</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #ff4444;">✗ Connection Failed</h1>
            <p>{str(e)}</p>
            <p>You can close this window now.</p>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)


@router.post("/zoom-webhook")
async def zoom_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_zm_signature: Optional[str] = Header(None),
    x_zm_request_timestamp: Optional[str] = Header(None)
):
    """Handle Zoom webhook events"""
    
    body = await request.body()
    data = await request.json()
    
    # Verify signature if configured
    if x_zm_signature and x_zm_request_timestamp:
        if not zoom_service.verify_webhook_signature(body, x_zm_signature, x_zm_request_timestamp):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    event_data = zoom_service.parse_webhook_event(data)
    
    if event_data.get("event_type") == "recording.completed":
        # Create meeting from Zoom recording
        meeting = Meeting(
            title=event_data.get("topic", "Zoom Meeting"),
            source_type="zoom",
            status="uploaded"
        )
        
        db.add(meeting)
        await db.commit()
        
        # In production: Download recording file and process
        
        return {"status": "received", "meeting_id": meeting.id}
    
    return {"status": "received"}


# ==================== MICROSOFT TEAMS INTEGRATION ====================

@router.get("/teams/auth")
async def teams_auth():
    """Initiate Microsoft Teams OAuth flow"""
    state = secrets.token_urlsafe(32)
    redirect_uri = "http://localhost:8000/api/integrations/teams/callback"
    
    auth_url = teams_service.get_authorization_url(redirect_uri, state)
    return {"authorization_url": auth_url, "state": state}


@router.get("/teams/callback")
async def teams_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Handle Teams OAuth callback"""
    try:
        redirect_uri = "http://localhost:8000/api/integrations/teams/callback"
        
        # Exchange code for tokens
        token_data = await teams_service.exchange_code_for_token(code, redirect_uri)
        
        # Get user info
        user_info = await teams_service.get_user_info(token_data["access_token"])
        
        # Store tokens in database
        
        html_content = """
        <html>
        <head><title>Teams Connected!</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #6264A7;">✓ Teams Connected Successfully!</h1>
            <p>You can close this window now.</p>
            <script>
                setTimeout(() => window.close(), 2000);
            </script>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)
    
    except Exception as e:
        html_content = f"""
        <html>
        <head><title>Connection Failed</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1 style="color: #ff4444;">✗ Connection Failed</h1>
            <p>{str(e)}</p>
            <p>You can close this window now.</p>
        </body>
        </html>
        """
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_content)


@router.post("/teams-webhook")
async def teams_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Microsoft Teams webhook events"""
    
    data = await request.json()
    
    # Handle Teams specific events via Graph API subscriptions
    # Create meeting from Teams recording
    
    return {"status": "received"}


# ==================== GENERIC WEBHOOK ====================

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
        status="uploaded" if data.get("transcript") else "pending"
    )
    
    # Handle metadata
    metadata = data.get("metadata", {})
    if "participants" in metadata:
        meeting.participants = metadata["participants"]
    
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    
    # If transcript provided, queue for processing
    if data.get("transcript"):
        # Background task would process here
        meeting.status = "processing"
        await db.commit()
    
    return {
        "status": "created",
        "meeting_id": meeting.id,
        "message": "Meeting created and queued for processing"
    }
