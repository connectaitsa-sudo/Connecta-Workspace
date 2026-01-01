import { useState } from 'react';
import { Settings as SettingsIcon, Key, Bell, Globe, Shield, Save, Check } from 'lucide-react';
import './Settings.css';

function Settings() {
  const [apiKey, setApiKey] = useState('sk-proj-rkO5gq...configured');
  const [language, setLanguage] = useState('en');
  const [reportLanguage, setReportLanguage] = useState('bilingual');
  const [notifications, setNotifications] = useState(true);
  const [saved, setSaved] = useState(false);

  const saveSettings = () => {
    // Save to localStorage or backend
    localStorage.setItem('settings', JSON.stringify({
      language,
      reportLanguage,
      notifications
    }));
    
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

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
            <div className="api-status">
              <span className="badge badge-success">
                <Check size={12} /> API Key Configured
              </span>
              <code className="api-key-display">{apiKey}</code>
            </div>
            <p className="help-text">
              To update: Edit <code>backend/.env</code> file
            </p>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Bell size={24} />
          </div>
          <div className="section-content">
            <h2>Notifications</h2>
            <p>Control email and in-app notifications</p>
            <div className="setting-control">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={notifications}
                  onChange={(e) => setNotifications(e.target.checked)}
                  className="toggle-input"
                />
                <span className="toggle-slider"></span>
                <span>Enable notifications when meetings are processed</span>
              </label>
            </div>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Globe size={24} />
          </div>
          <div className="section-content">
            <h2>Language & Region</h2>
            <p>Set your preferred language and report generation settings</p>
            
            <div className="setting-group">
              <label htmlFor="interface-language">Interface Language</label>
              <select
                id="interface-language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="setting-select"
              >
                <option value="en">English</option>
                <option value="ar">Arabic (العربية)</option>
                <option value="ur">Urdu (اردو)</option>
                <option value="hi">Hindi (हिन्दी)</option>
              </select>
            </div>

            <div className="setting-group">
              <label htmlFor="report-language">Report Generation Language</label>
              <select
                id="report-language"
                value={reportLanguage}
                onChange={(e) => setReportLanguage(e.target.value)}
                className="setting-select"
              >
                <option value="bilingual">Bilingual (English + Arabic)</option>
                <option value="en">English Only</option>
                <option value="ar">Arabic Only (العربية)</option>
                <option value="ur">Urdu Only (اردو)</option>
                <option value="hi">Hindi Only (हिन्दी)</option>
              </select>
              <p className="help-text">
                Bilingual mode generates reports in both English and Arabic
              </p>
            </div>
          </div>
        </div>

        <div className="settings-section">
          <div className="section-icon">
            <Shield size={24} />
          </div>
          <div className="section-content">
            <h2>Privacy & Security</h2>
            <p>Manage your data and security settings</p>
            <ul className="privacy-list">
              <li>✓ All data stored locally</li>
              <li>✓ OpenAI does not store your audio/transcripts</li>
              <li>✓ HTTPS encryption in production</li>
              <li>✓ No data shared with third parties</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="settings-footer">
        <button 
          className={`btn btn-primary btn-lg ${saved ? 'btn-success' : ''}`}
          onClick={saveSettings}
        >
          {saved ? (
            <>
              <Check size={18} />
              Saved Successfully!
            </>
          ) : (
            <>
              <Save size={18} />
              Save Settings
            </>
          )}
        </button>
      </div>
    </div>
  );
}

export default Settings;
