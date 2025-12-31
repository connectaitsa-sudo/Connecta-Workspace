import { Zap, Video, Users, Link as LinkIcon } from 'lucide-react';
import './Integrations.css';

function Integrations() {
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
              <span className="badge badge-info">Coming Soon</span>
            </div>
            <button className="btn btn-secondary" disabled>
              Connect Zoom
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
              <span className="badge badge-info">Coming Soon</span>
            </div>
            <button className="btn btn-secondary" disabled>
              Connect Teams
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
