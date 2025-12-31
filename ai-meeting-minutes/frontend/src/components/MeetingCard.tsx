import { Clock, Users, Calendar, CheckCircle, Loader, AlertCircle } from 'lucide-react';
import { Meeting } from '../types';
import './MeetingCard.css';

interface MeetingCardProps {
  meeting: Meeting;
  onClick: () => void;
}

function MeetingCard({ meeting, onClick }: MeetingCardProps) {
  const getStatusBadge = () => {
    switch (meeting.status) {
      case 'completed':
        return <span className="badge badge-success"><CheckCircle size={12} /> Completed</span>;
      case 'processing':
      case 'transcribing':
        return <span className="badge badge-warning"><Loader size={12} className="animate-spin" /> Processing</span>;
      case 'failed':
        return <span className="badge badge-error"><AlertCircle size={12} /> Failed</span>;
      default:
        return <span className="badge badge-info">Uploaded</span>;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <div className="meeting-card" onClick={onClick}>
      <div className="meeting-card-header">
        <h3 className="meeting-card-title">
          {meeting.title || `Meeting #${meeting.id}`}
        </h3>
        {getStatusBadge()}
      </div>

      {meeting.summary && (
        <p className="meeting-card-summary">
          {meeting.summary.length > 150
            ? meeting.summary.substring(0, 150) + '...'
            : meeting.summary}
        </p>
      )}

      <div className="meeting-card-meta">
        {meeting.duration_minutes && (
          <div className="meta-item">
            <Clock size={14} />
            <span>{Math.round(meeting.duration_minutes)} min</span>
          </div>
        )}

        {meeting.participants && meeting.participants.length > 0 && (
          <div className="meta-item">
            <Users size={14} />
            <span>{meeting.participants.length} participants</span>
          </div>
        )}

        <div className="meta-item">
          <Calendar size={14} />
          <span>{formatDate(meeting.created_at)}</span>
        </div>
      </div>

      {meeting.key_points && meeting.key_points.length > 0 && (
        <div className="meeting-card-tags">
          <span className="tag">{meeting.key_points.length} key points</span>
          {meeting.action_items && meeting.action_items.length > 0 && (
            <span className="tag">{meeting.action_items.length} action items</span>
          )}
        </div>
      )}
    </div>
  );
}

export default MeetingCard;
