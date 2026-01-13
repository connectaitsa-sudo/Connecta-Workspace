"""Microsoft Teams integration service with Graph API"""

import httpx
from typing import Optional, Dict, Any, List
from app.core.config import settings


class TeamsService:
    """Service for Microsoft Teams integration"""
    
    def __init__(self):
        self.client_id = settings.TEAMS_CLIENT_ID
        self.client_secret = settings.TEAMS_CLIENT_SECRET
        self.tenant_id = settings.TEAMS_TENANT_ID if hasattr(settings, 'TEAMS_TENANT_ID') else 'common'
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self.auth_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0"
        
        # Required scopes
        self.scopes = [
            "OnlineMeetings.Read.All",
            "OnlineMeetingRecording.Read.All",
            "CallRecords.Read.All",
            "User.Read"
        ]
    
    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        Generate Microsoft Teams OAuth authorization URL
        
        Args:
            redirect_uri: Where to redirect after authorization
            state: CSRF protection state parameter
        
        Returns:
            Authorization URL for user to visit
        """
        scope_string = " ".join(self.scopes)
        return (
            f"{self.auth_url}/authorize?"
            f"client_id={self.client_id}&"
            f"response_type=code&"
            f"redirect_uri={redirect_uri}&"
            f"response_mode=query&"
            f"scope={scope_string}&"
            f"state={state}"
        )
    
    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Microsoft
            redirect_uri: Same redirect URI used in authorization
        
        Returns:
            Dictionary with access_token, refresh_token, etc.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.auth_url}/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            return response.json()
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh expired access token"""
        scope_string = " ".join(self.scopes)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.auth_url}/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                    "scope": scope_string
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get Teams user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.graph_url}/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
    
    async def list_online_meetings(
        self,
        access_token: str,
        user_id: str = "me"
    ) -> List[Dict[str, Any]]:
        """
        List online meetings for a user
        
        Args:
            access_token: OAuth access token
            user_id: User ID or 'me' for current user
        
        Returns:
            List of online meetings
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.graph_url}/users/{user_id}/onlineMeetings",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json().get("value", [])
    
    async def get_meeting_recording(
        self,
        access_token: str,
        meeting_id: str
    ) -> Dict[str, Any]:
        """Get meeting recording details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.graph_url}/me/onlineMeetings/{meeting_id}/recordings",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_call_records(
        self,
        access_token: str,
        from_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get call records (includes recordings)
        
        Args:
            access_token: OAuth access token
            from_date: Filter by date (ISO 8601 format)
        
        Returns:
            List of call records
        """
        url = f"{self.graph_url}/communications/callRecords"
        if from_date:
            url += f"?$filter=startDateTime ge {from_date}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            response.raise_for_status()
            return response.json().get("value", [])
    
    async def download_recording(
        self,
        access_token: str,
        recording_url: str,
        output_path: str
    ) -> str:
        """
        Download Teams recording
        
        Args:
            access_token: OAuth access token
            recording_url: URL to download from
            output_path: Where to save the file
        
        Returns:
            Path to downloaded file
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                recording_url,
                headers={"Authorization": f"Bearer {access_token}"},
                follow_redirects=True
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
    
    async def subscribe_to_notifications(
        self,
        access_token: str,
        notification_url: str,
        resource: str = "communications/onlineMeetings"
    ) -> Dict[str, Any]:
        """
        Subscribe to change notifications
        
        Args:
            access_token: OAuth access token
            notification_url: Where to send notifications
            resource: Resource to watch
        
        Returns:
            Subscription details
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.graph_url}/subscriptions",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "changeType": "created,updated",
                    "notificationUrl": notification_url,
                    "resource": resource,
                    "expirationDateTime": "2024-12-31T23:59:00.0000000Z",
                    "clientState": "secretClientValue"
                }
            )
            response.raise_for_status()
            return response.json()


# Singleton instance
teams_service = TeamsService()
