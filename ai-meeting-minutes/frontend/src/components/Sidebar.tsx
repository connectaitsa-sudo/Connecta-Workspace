import {
  LayoutDashboard,
  Plus,
  Link as LinkIcon,
  Settings as SettingsIcon,
  FileText,
  Zap
} from 'lucide-react';
import './Sidebar.css';

interface SidebarProps {
  currentView: string;
  onNavigate: (view: any) => void;
}

function Sidebar({ currentView, onNavigate }: SidebarProps) {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard', badge: null },
    { id: 'new-meeting', icon: Plus, label: 'New Meeting', badge: null },
    { id: 'integrations', icon: LinkIcon, label: 'Integrations', badge: 'Beta' },
    { id: 'settings', icon: SettingsIcon, label: 'Settings', badge: null },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <FileText size={28} />
          <div>
            <h1 className="sidebar-title">Meeting AI</h1>
            <p className="sidebar-subtitle">Enterprise Edition</p>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-item ${currentView === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <item.icon size={20} />
            <span>{item.label}</span>
            {item.badge && <span className="sidebar-badge">{item.badge}</span>}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-card">
          <Zap size={20} className="sidebar-card-icon" />
          <h3 className="sidebar-card-title">Upgrade to Pro</h3>
          <p className="sidebar-card-text">
            Unlock unlimited meetings, advanced analytics, and priority support.
          </p>
          <button className="sidebar-card-button">Upgrade Now</button>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
