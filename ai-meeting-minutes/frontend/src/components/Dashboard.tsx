import { useState } from 'react';
import {
  Search,
  Filter,
  Calendar,
  Clock,
  Users,
  FileText,
  TrendingUp,
  Plus,
  RefreshCw
} from 'lucide-react';
import { Meeting } from '../types';
import MeetingCard from './MeetingCard';
import './Dashboard.css';

interface DashboardProps {
  meetings: Meeting[];
  loading: boolean;
  onViewMeeting: (meeting: Meeting) => void;
  onRefresh: () => void;
}

function Dashboard({ meetings, loading, onViewMeeting, onRefresh }: DashboardProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');

  const filteredMeetings = meetings.filter(meeting => {
    const matchesSearch = meeting.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         meeting.summary?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesFilter = filterStatus === 'all' || meeting.status === filterStatus;
    
    return matchesSearch && matchesFilter;
  });

  // Calculate stats
  const completedMeetings = meetings.filter(m => m.status === 'completed').length;
  const totalDuration = meetings
    .filter(m => m.duration_minutes)
    .reduce((sum, m) => sum + (m.duration_minutes || 0), 0);
  const totalParticipants = new Set(
    meetings.flatMap(m => m.participants || [])
  ).size;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">
            Manage and review your meeting minutes
          </p>
        </div>
        <button className="btn btn-primary" onClick={onRefresh}>
          <RefreshCw size={18} />
          Refresh
        </button>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#dbeafe', color: '#1e40af' }}>
            <FileText size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Total Meetings</p>
            <p className="stat-value">{meetings.length}</p>
            <p className="stat-change">
              <TrendingUp size={14} />
              <span>+12% from last month</span>
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#d1fae5', color: '#065f46' }}>
            <Clock size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Total Duration</p>
            <p className="stat-value">{Math.round(totalDuration)} min</p>
            <p className="stat-change">
              <TrendingUp size={14} />
              <span>{Math.round(totalDuration / 60)}h recorded</span>
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#fef3c7', color: '#92400e' }}>
            <Users size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Participants</p>
            <p className="stat-value">{totalParticipants}</p>
            <p className="stat-change">
              <TrendingUp size={14} />
              <span>Unique members</span>
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ background: '#e0e7ff', color: '#3730a3' }}>
            <Calendar size={24} />
          </div>
          <div className="stat-content">
            <p className="stat-label">Completed</p>
            <p className="stat-value">{completedMeetings}</p>
            <p className="stat-change">
              <TrendingUp size={14} />
              <span>{Math.round((completedMeetings / meetings.length) * 100 || 0)}% success rate</span>
            </p>
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="dashboard-filters">
        <div className="search-box">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search meetings..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        <div className="filter-group">
          <Filter size={18} />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Status</option>
            <option value="completed">Completed</option>
            <option value="processing">Processing</option>
            <option value="failed">Failed</option>
          </select>
        </div>
      </div>

      {/* Meetings List */}
      <div className="meetings-section">
        <h2 className="section-title">Recent Meetings</h2>

        {loading ? (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading meetings...</p>
          </div>
        ) : filteredMeetings.length === 0 ? (
          <div className="empty-state">
            <FileText size={64} className="empty-icon" />
            <h3>No meetings found</h3>
            <p>
              {searchQuery || filterStatus !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Get started by creating your first meeting'}
            </p>
            {!searchQuery && filterStatus === 'all' && (
              <button className="btn btn-primary">
                <Plus size={18} />
                Create Meeting
              </button>
            )}
          </div>
        ) : (
          <div className="meetings-grid">
            {filteredMeetings.map((meeting) => (
              <MeetingCard
                key={meeting.id}
                meeting={meeting}
                onClick={() => onViewMeeting(meeting)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
