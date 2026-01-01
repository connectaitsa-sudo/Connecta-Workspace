# 🔗 Integration Guide - Connect with Zoom, Teams & More

Complete step-by-step guide to connect your meeting platforms.

---

## 📹 Zoom Integration

### Step 1: Create Zoom App

1. Go to https://marketplace.zoom.us/
2. Click **"Develop"** → **"Build App"**
3. Choose **"OAuth"** app type
4. Fill in basic information:
   - App Name: "AI Meeting Minutes"
   - Company Name: Your name
   - Developer Email: Your email

### Step 2: Configure OAuth

1. In **"OAuth"** section:
   - Redirect URL: `http://localhost:8000/api/integrations/zoom/callback`
   - Add URL to allowlist
   
2. Copy **Client ID** and **Client Secret**

3. In **"Scopes"** section, add:
   - `recording:read:admin`
   - `recording:write:admin`
   - `meeting:read:admin`
   - `cloud_recording:read:admin`

### Step 3: Setup Webhook

1. In **"Feature"** → **"Event Subscriptions"**:
   - Event notification endpoint: `http://localhost:8000/api/integrations/zoom-webhook`
   
2. Subscribe to events:
   - `recording.completed`
   - `recording.transcript_completed`
   
3. Copy **Verification Token**

### Step 4: Configure Backend

Edit `backend/.env`:

```env
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret
ZOOM_WEBHOOK_SECRET=your_verification_token
```

### Step 5: Test Connection

1. Restart backend: `python run.py`
2. Go to http://localhost:3000
3. Click **"Integrations"**
4. Click **"Connect Zoom"**
5. Authorize the app

### ✅ Done! Zoom recordings will auto-import

---

## 👥 Microsoft Teams Integration

### Step 1: Register App in Azure

1. Go to https://portal.azure.com/
2. Navigate to **"Azure Active Directory"**
3. Click **"App registrations"** → **"New registration"**
4. Fill in:
   - Name: "AI Meeting Minutes"
   - Redirect URI: `http://localhost:8000/api/integrations/teams/callback`

### Step 2: Configure Permissions

1. Go to **"API permissions"**
2. Click **"Add a permission"** → **"Microsoft Graph"**
3. Add these permissions:
   - `OnlineMeetings.Read.All`
   - `OnlineMeetingRecording.Read.All`
   - `CallRecords.Read.All`
   - `User.Read`

4. Click **"Grant admin consent"**

### Step 3: Create Client Secret

1. Go to **"Certificates & secrets"**
2. Click **"New client secret"**
3. Copy the secret value (you won't see it again!)

### Step 4: Get IDs

1. From **"Overview"** page, copy:
   - **Application (client) ID**
   - **Directory (tenant) ID**

### Step 5: Configure Backend

Edit `backend/.env`:

```env
TEAMS_CLIENT_ID=your_application_id
TEAMS_CLIENT_SECRET=your_client_secret
TEAMS_TENANT_ID=your_tenant_id
```

### Step 6: Test Connection

1. Restart backend
2. Go to Integrations page
3. Click **"Connect Teams"**
4. Sign in with Microsoft account

### ✅ Done! Teams meetings will auto-sync

---

## 🎥 Google Meet Integration

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Create new project: "AI Meeting Minutes"
3. Enable **Google Meet API**

### Step 2: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Choose **"Web application"**
4. Add redirect URI: `http://localhost:8000/api/integrations/meet/callback`

### Step 3: Configure Scopes

Add these scopes:
- `https://www.googleapis.com/auth/meetings.space.readonly`
- `https://www.googleapis.com/auth/drive.readonly`

### Step 4: Configure Backend

Edit `backend/.env`:

```env
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
```

### ✅ Done! Google Meet recordings accessible

---

## 🌐 Generic Webhook Integration

For any other platform:

### Webhook URL:
```
POST http://localhost:8000/api/integrations/generic-webhook
```

### Request Format:

```json
{
  "title": "Meeting Title",
  "audio_url": "https://example.com/recording.mp3",
  "transcript": "Optional transcript text",
  "metadata": {
    "participants": ["John", "Sarah"],
    "date": "2024-01-01T10:00:00Z",
    "duration": 3600
  }
}
```

### Response:

```json
{
  "status": "created",
  "meeting_id": 123,
  "message": "Meeting created and queued for processing"
}
```

### Example with cURL:

```bash
curl -X POST http://localhost:8000/api/integrations/generic-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "audio_url": "https://example.com/meeting.mp3",
    "metadata": {
      "participants": ["Alice", "Bob"]
    }
  }'
```

---

## 🔧 Testing Integration

### Test Zoom:

```bash
# Start a Zoom meeting
# Enable cloud recording
# End meeting
# Wait 5-10 minutes
# Check your dashboard - recording should appear!
```

### Test Teams:

```bash
# Start Teams meeting
# Record the meeting
# End meeting
# Recording will sync automatically
```

### Test Webhook:

```bash
curl -X POST http://localhost:8000/api/integrations/generic-webhook \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Meeting",
    "transcript": "John: Hello everyone. Sarah: Hi team!"
  }'
```

---

## 🎯 Production Deployment

### For Production URLs:

1. **Get a domain**: yourapp.com
2. **Setup HTTPS** (required for OAuth)
3. **Update redirect URLs** in all platforms:
   - Zoom: `https://yourapp.com/api/integrations/zoom/callback`
   - Teams: `https://yourapp.com/api/integrations/teams/callback`
   - Meet: `https://yourapp.com/api/integrations/meet/callback`

4. **Update webhook URLs**:
   - Zoom: `https://yourapp.com/api/integrations/zoom-webhook`

5. **Update .env** with production URLs

---

## 🔐 Security Best Practices

1. ✅ Never commit `.env` file to git
2. ✅ Use HTTPS in production
3. ✅ Rotate secrets regularly
4. ✅ Limit OAuth scopes to minimum required
5. ✅ Validate webhook signatures
6. ✅ Use environment variables
7. ✅ Enable rate limiting

---

## 🆘 Troubleshooting

### Zoom Connection Fails

**Problem**: Redirect URI mismatch

**Solution**: 
- Make sure URL in Zoom app matches exactly
- Include port number: `:8000`
- No trailing slash

### Teams Returns 403

**Problem**: Permissions not granted

**Solution**:
- Go to Azure portal
- Click "Grant admin consent"
- Wait 5 minutes
- Try again

### Webhook Not Receiving Data

**Problem**: URL not accessible

**Solution for Development**:
- Use ngrok to expose localhost:
  ```bash
  ngrok http 8000
  ```
- Update webhook URL with ngrok URL

### API Key Invalid

**Problem**: Old or incorrect key

**Solution**:
- Generate new key at https://platform.openai.com/api-keys
- Update `backend/.env`
- Restart backend

---

## 📊 How It Works

```
┌─────────────┐
│   Zoom      │──┐
└─────────────┘  │
                 │
┌─────────────┐  │    ┌──────────────┐    ┌─────────────┐
│   Teams     │──┼───→│   Webhook    │───→│   Backend   │
└─────────────┘  │    │   Receiver   │    │   Server    │
                 │    └──────────────┘    └─────────────┘
┌─────────────┐  │                              │
│ Google Meet │──┘                              │
└─────────────┘                                 ↓
                                        ┌─────────────┐
                                        │   OpenAI    │
                                        │   Whisper   │
                                        │   + GPT-4   │
                                        └─────────────┘
                                                ↓
                                        ┌─────────────┐
                                        │   Meeting   │
                                        │   Minutes   │
                                        └─────────────┘
```

---

## 🎓 Video Tutorials

### Zoom Setup:
1. Record your screen while following steps
2. Share with team

### Teams Setup:
1. Follow Azure portal steps
2. Document any errors

---

## 💡 Tips

1. **Start with Generic Webhook** - Easiest to test
2. **Use ngrok for development** - Makes localhost accessible
3. **Test with short recordings first** - Save API costs
4. **Monitor logs** - Check backend terminal for errors
5. **Read platform docs** - Each has specific requirements

---

## ✅ Checklist

Before going live:

- [ ] Zoom app created and configured
- [ ] Teams app registered in Azure
- [ ] OAuth redirect URLs correct
- [ ] Webhook URLs accessible
- [ ] API keys in .env file
- [ ] Backend restarted after config
- [ ] Test recording processed successfully
- [ ] Production URLs updated (if deploying)

---

## 🚀 Next Steps

1. **Setup one integration** (start with easiest for you)
2. **Test with real meeting**
3. **Monitor first few recordings**
4. **Configure remaining platforms**
5. **Share with team**

---

**Need Help?** Check backend logs: `backend terminal window`

**Working!** 🎉 Your meetings will now auto-import and generate minutes!
