"""Zoom integration service with OAuth and webhook support"""

import httpx
import hmac
import hashlib
from typing import Optional, Dict, Any
from app.core.config import settings


class ZoomService:
    """Service for Zoom integration"""
    
    def __init__(self):
        self.client_id = settings.ZOOM_CLIENT_ID
        self.client_secret = settings.ZOOM_CLIENT_SECRET
        self.webhook_secret = settings.ZOOM_WEBHOOK_SECRET
        self.base_url = "https://api.zoom.us/v2"
        self.oauth_url = "https://zoom.us/oauth"
    
    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate Zoom OAuth authorization URL
        
        Args:
            redirect_uri: Where to redirect after authorization
            state: CSRF protection state parameter
        
        Returns:
            Authorization URL for user to visit
        """
        return (
            f"{self.oauth_url}/authorize?"
            f"response_type=code&"
            f"client_id={self.client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"state={state}"
        )
    
    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Zoom
            redirect_uri: Same redirect URI used in authorization
        
        Returns:
            Dictionary with access_token, refresh_token, etc.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.oauth_url}/token",
                auth=(self.client_id, self.client_secret),
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh expired access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.oauth_url}/token",
                auth=(self.client_id, self.client_secret),
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Zoom user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
    
    async def list_recordings(
        self,
        access_token: str,
        user_id: str = "me",
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List cloud recordings for a user
        
        Args:
            access_token: OAuth access token
            user_id: Zoom user ID or 'me' for current user
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
        
        Returns:
            List of recordings
        """
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/{user_id}/recordings",
                headers={"Authorization": f"Bearer {access_token}"},
                params=params
            )
            response.raise_for_status()
            return response.json()
    
    async def get_recording(
        self,
        access_token: str,
        meeting_id: str
    ) -> Dict[str, Any]:
        """Get specific recording details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/meetings/{meeting_id}/recordings",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
    
    async def download_recording(
        self,
        access_token: str,
        download_url: str,
        output_path: str
    ) -> str:
        """
        Download recording file
        
        Args:
            access_token: OAuth access token
            download_url: URL to download from
            output_path: Where to save the file
        
        Returns:
            Path to downloaded file
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                download_url,
                headers={"Authorization": f"Bearer {access_token}"},
                follow_redirects=True
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
    
    def verify_webhook_signature(
        self,
        request_body: bytes,
        signature: str,
        timestamp: str
    ) -> bool:
        """
        Verify Zoom webhook signature
        
        Args:
            request_body: Raw request body
            signature: Signature from x-zm-signature header
            timestamp: Timestamp from x-zm-request-timestamp header
        
        Returns:
            True if signature is valid
        """
        if not self.webhook_secret:
            return True  # Skip verification if not configured
        
        # Construct message
        message = f"v0:{timestamp}:{request_body.decode()}"
        
        # Calculate HMAC
        hash_for_verify = hmac.new(
            self.webhook_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        expected_signature = f"v0={hash_for_verify}"
        
        return hmac.compare_digest(signature, expected_signature)
    
    def parse_webhook_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Zoom webhook event
        
        Args:
            payload: Webhook payload from Zoom
        
        Returns:
            Parsed event data
        """
        event_type = payload.get("event")
        event_data = {}
        
        if event_type == "recording.completed":
            meeting = payload.get("payload", {}).get("object", {})
            event_data = {
                "event_type": "recording.completed",
                "meeting_id": meeting.get("id"),
                "uuid": meeting.get("uuid"),
                "host_id": meeting.get("host_id"),
                "topic": meeting.get("topic"),
                "start_time": meeting.get("start_time"),
                "duration": meeting.get("duration"),
                "recording_files": meeting.get("recording_files", [])
            }
        
        elif event_type == "recording.transcript_completed":
            recording = payload.get("payload", {}).get("object", {})
            event_data = {
                "event_type": "recording.transcript_completed",
                "meeting_id": recording.get("id"),
                "uuid": recording.get("uuid"),
                "transcript_file": recording.get("transcript_file")
            }
        
        return event_data


# Singleton instance
zoom_service = ZoomService()
