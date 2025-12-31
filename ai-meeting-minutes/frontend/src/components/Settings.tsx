import { Settings as SettingsIcon, Key, Bell, Globe, Shield } from 'lucide-react';
import './Settings.css';

function Settings() {
  return (
    <div className="settings">
      <div className="settings-header">
        <h1 className="page-title">Settings</h1>
        <p className="page-subtitle">Manage your preferences</p>
      </div>

      <div className="settings-content">
        <div className="settings-section">
          <div className="section-icon">
            <Key size={24} />
          </div>
          <div className="section-content">
            <h2>API Configuration</h2>
            <p>Configure your OpenAI API key and other integration settings</p>
            <button className="btn btn-secondary">Manage API Keys</button>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Bell size={24} />
          </div>
          <div className="section-content">
            <h2>Notifications</h2>
            <p>Control email and in-app notifications</p>
            <button className="btn btn-secondary">Configure Notifications</button>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Globe size={24} />
          </div>
          <div className="section-content">
            <h2>Language & Region</h2>
            <p>Set your preferred language and time zone</p>
            <button className="btn btn-secondary">Update Preferences</button>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Shield size={24} />
          </div>
          <div className="section-content">
            <h2>Privacy & Security</h2>
            <p>Manage your data and security settings</p>
            <button className="btn btn-secondary">Privacy Settings</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
