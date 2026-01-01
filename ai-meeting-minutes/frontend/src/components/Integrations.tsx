import { useState } from 'react';
import { Zap, Video, Users, Link as LinkIcon, ExternalLink, Check } from 'lucide-react';
import axios from 'axios';
import './Integrations.css';

function Integrations() {
  const [zoomConnected, setZoomConnected] = useState(false);
  const [teamsConnected, setTeamsConnected] = useState(false);
  const [loading, setLoading] = useState<string | null>(null);

  const connectZoom = async () => {
    setLoading('zoom');
    try {
      const response = await axios.get('http://localhost:8000/api/integrations/zoom/auth');
      const authUrl = response.data.authorization_url;
      
      // Open in popup
      const popup = window.open(authUrl, 'Zoom Authorization', 'width=600,height=700');
      
      // Listen for popup close or success
      const checkPopup = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkPopup);
          setZoomConnected(true);
          setLoading(null);
        }
      }, 500);
    } catch (error) {
      console.error('Zoom connection error:', error);
      alert('Failed to connect Zoom. Please check backend logs.');
      setLoading(null);
    }
  };

  const connectTeams = async () => {
    setLoading('teams');
    try {
      const response = await axios.get('http://localhost:8000/api/integrations/teams/auth');
      const authUrl = response.data.authorization_url;
      
      // Open in popup
      const popup = window.open(authUrl, 'Teams Authorization', 'width=600,height=700');
      
      // Listen for popup close or success
      const checkPopup = setInterval(() => {
        if (popup?.closed) {
          clearInterval(checkPopup);
          setTeamsConnected(true);
          setLoading(null);
        }
      }, 500);
    } catch (error) {
      console.error('Teams connection error:', error);
      alert('Failed to connect Teams. Please check backend logs.');
      setLoading(null);
    }
  };

  return (
    <div className="integrations">
      <div className="integrations-header">
        <h1 className="page-title">Integrations</h1>
        <p className="page-subtitle">Connect your meeting platforms</p>
      </div>

      <div className="integrations-grid">
        <div className="integration-card">
          <div className="integration-icon" style={{ background: '#4285F4' }}>
            <Video size={32} color="white" />
          </div>
          <div className="integration-content">
            <h3 className="integration-title">Zoom</h3>
            <p className="integration-description">
              Automatically import and transcribe your Zoom meeting recordings
            </p>
            <div className="integration-status">
              {zoomConnected ? (
                <span className="badge badge-success">
                  <Check size={12} /> Connected
                </span>
              ) : (
                <span className="badge badge-info">Ready to Connect</span>
              )}
            </div>
            <button 
              className={`btn ${zoomConnected ? 'btn-success' : 'btn-primary'}`}
              onClick={connectZoom}
              disabled={loading === 'zoom' || zoomConnected}
            >
              {loading === 'zoom' ? 'Connecting...' : zoomConnected ? 'Connected' : 'Connect Zoom'}
              {!zoomConnected && <ExternalLink size={16} />}
            </button>
          </div>
        </div>

        <div className="integration-card">
          <div className="integration-icon" style={{ background: '#6264A7' }}>
            <Users size={32} color="white" />
          </div>
          <div className="integration-content">
            <h3 className="integration-title">Microsoft Teams</h3>
            <p className="integration-description">
              Sync your Teams meetings and generate minutes automatically
            </p>
            <div className="integration-status">
              {teamsConnected ? (
                <span className="badge badge-success">
                  <Check size={12} /> Connected
                </span>
              ) : (
                <span className="badge badge-info">Ready to Connect</span>
              )}
            </div>
            <button 
              className={`btn ${teamsConnected ? 'btn-success' : 'btn-primary'}`}
              onClick={connectTeams}
              disabled={loading === 'teams' || teamsConnected}
            >
              {loading === 'teams' ? 'Connecting...' : teamsConnected ? 'Connected' : 'Connect Teams'}
              {!teamsConnected && <ExternalLink size={16} />}
            </button>
          </div>
        </div>

        <div className="integration-card">
          <div className="integration-icon" style={{ background: '#00B37D' }}>
            <LinkIcon size={32} color="white" />
          </div>
          <div className="integration-content">
            <h3 className="integration-title">Google Meet</h3>
            <p className="integration-description">
              Import recordings from Google Meet automatically
            </p>
            <div className="integration-status">
              <span className="badge badge-info">Coming Soon</span>
            </div>
            <button className="btn btn-secondary" disabled>
              Connect Google Meet
            </button>
          </div>
        </div>

        <div className="integration-card">
          <div className="integration-icon" style={{ background: '#FF6B6B' }}>
            <Zap size={32} color="white" />
          </div>
          <div className="integration-content">
            <h3 className="integration-title">Webhook</h3>
            <p className="integration-description">
              Use our webhook API to integrate with any platform
            </p>
            <div className="integration-status">
              <span className="badge badge-success">Available</span>
            </div>
            <button className="btn btn-primary">
              View Documentation
            </button>
          </div>
        </div>
      </div>

      <div className="integrations-info">
        <h2>How Integrations Work</h2>
        <p>
          Connect your meeting platforms to automatically import recordings and generate meeting minutes. 
          All integrations use secure OAuth authentication and respect your data privacy.
        </p>
        <ul>
          <li>✅ Automatic meeting detection</li>
          <li>✅ Secure OAuth 2.0 authentication</li>
          <li>✅ Real-time sync</li>
          <li>✅ Privacy-first approach</li>
        </ul>
      </div>
    </div>
  );
}

export default Integrations;
