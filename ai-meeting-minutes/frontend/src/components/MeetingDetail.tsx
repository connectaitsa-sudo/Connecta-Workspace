import { useState, useEffect } from 'react';
import { ArrowLeft, Download, RefreshCw, Trash2, Clock, Users, Calendar } from 'lucide-react';
import { Meeting } from '../types';
import { getMeeting, exportMeeting, deleteMeeting } from '../api';
import './MeetingDetail.css';

interface MeetingDetailProps {
  meeting: Meeting;
  onBack: () => void;
  onMeetingUpdated: (meeting: Meeting) => void;
  onMeetingDeleted: (meetingId: number) => void;
}

function MeetingDetail({ meeting: initialMeeting, onBack, onMeetingUpdated, onMeetingDeleted }: MeetingDetailProps) {
  const [meeting, setMeeting] = useState<Meeting>(initialMeeting);
  const [isPolling, setIsPolling] = useState(false);
  const [exportingFormat, setExportingFormat] = useState<string | null>(null);

  useEffect(() => {
    setMeeting(initialMeeting);
    
    if (['uploaded', 'transcribing', 'processing'].includes(initialMeeting.status)) {
      setIsPolling(true);
    }
  }, [initialMeeting]);

  useEffect(() => {
    if (!isPolling) return;

    const pollInterval = setInterval(async () => {
      try {
        const updated = await getMeeting(meeting.id);
        setMeeting(updated);
        onMeetingUpdated(updated);

        if (updated.status === 'completed' || updated.status === 'failed') {
          setIsPolling(false);
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [isPolling, meeting.id]);

  const handleExport = async (format: 'pdf' | 'docx' | 'txt') => {
    setExportingFormat(format);
    try {
      const blob = await exportMeeting(meeting.id, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `meeting-${meeting.id}-minutes.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export. Please try again.');
    } finally {
      setExportingFormat(null);
    }
  };

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this meeting?')) return;

    try {
      await deleteMeeting(meeting.id);
      onMeetingDeleted(meeting.id);
    } catch (error) {
      console.error('Delete error:', error);
      alert('Failed to delete meeting.');
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (meeting.status === 'processing' || meeting.status === 'transcribing') {
    return (
      <div className="meeting-detail">
        <div className="detail-header">
          <button className="btn-back" onClick={onBack}>
            <ArrowLeft size={20} />
            Back
          </button>
        </div>

        <div className="processing-state">
          <div className="spinner-large"></div>
          <h2>Processing Your Meeting...</h2>
          <p>
            {meeting.status === 'transcribing' ? 'Transcribing audio...' : 'Generating meeting minutes with AI...'}
          </p>
        </div>
      </div>
    );
  }

  if (meeting.status === 'failed') {
    return (
      <div className="meeting-detail">
        <div className="detail-header">
          <button className="btn-back" onClick={onBack}>
            <ArrowLeft size={20} />
            Back
          </button>
        </div>

        <div className="error-state">
          <h2>Processing Failed</h2>
          <p>{meeting.error_message || 'An error occurred while processing the meeting.'}</p>
          <button className="btn btn-primary" onClick={onBack}>
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="meeting-detail">
      <div className="detail-header">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} />
          Back
        </button>

        <div className="header-actions">
          <button
            className="btn btn-secondary"
            onClick={() => handleExport('pdf')}
            disabled={exportingFormat !== null}
          >
            <Download size={18} />
            {exportingFormat === 'pdf' ? 'Exporting...' : 'PDF'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => handleExport('docx')}
            disabled={exportingFormat !== null}
          >
            <Download size={18} />
            {exportingFormat === 'docx' ? 'Exporting...' : 'DOCX'}
          </button>
          <button
            className="btn btn-secondary"
            onClick={() => handleExport('txt')}
            disabled={exportingFormat !== null}
          >
            <Download size={18} />
            {exportingFormat === 'txt' ? 'Exporting...' : 'TXT'}
          </button>
          <button className="btn btn-danger" onClick={handleDelete}>
            <Trash2 size={18} />
            Delete
          </button>
        </div>
      </div>

      <div className="detail-content">
        <div className="detail-title-section">
          <h1 className="detail-title">{meeting.title || `Meeting #${meeting.id}`}</h1>
          
          <div className="detail-meta">
            {meeting.duration_minutes && (
              <div className="meta-item">
                <Clock size={16} />
                <span>{Math.round(meeting.duration_minutes)} minutes</span>
              </div>
            )}
            {meeting.participants && meeting.participants.length > 0 && (
              <div className="meta-item">
                <Users size={16} />
                <span>{meeting.participants.length} participants</span>
              </div>
            )}
            <div className="meta-item">
              <Calendar size={16} />
              <span>{formatDate(meeting.created_at)}</span>
            </div>
          </div>
        </div>

        {meeting.summary && (
          <div className="detail-section summary-section">
            <h2 className="section-title">Summary</h2>
            <p className="summary-text">{meeting.summary}</p>
          </div>
        )}

        {meeting.participants && meeting.participants.length > 0 && (
          <div className="detail-section">
            <h2 className="section-title">Participants</h2>
            <div className="participants-grid">
              {meeting.participants.map((participant, index) => (
                <div key={index} className="participant-chip">
                  {participant}
                </div>
              ))}
            </div>
          </div>
        )}

        {meeting.key_points && meeting.key_points.length > 0 && (
          <div className="detail-section">
            <h2 className="section-title">Key Discussion Points</h2>
            <ul className="points-list">
              {meeting.key_points.map((point, index) => (
                <li key={index}>{point}</li>
              ))}
            </ul>
          </div>
        )}

        {meeting.decisions && meeting.decisions.length > 0 && (
          <div className="detail-section decisions-section">
            <h2 className="section-title">Decisions Made</h2>
            <ul className="decisions-list">
              {meeting.decisions.map((decision, index) => (
                <li key={index}>{decision}</li>
              ))}
            </ul>
          </div>
        )}

        {meeting.action_items && meeting.action_items.length > 0 && (
          <div className="detail-section action-section">
            <h2 className="section-title">Action Items</h2>
            <div className="action-items-list">
              {meeting.action_items.map((item, index) => (
                <div key={index} className="action-item">
                  <div className="action-content">
                    <p className="action-description">{item.description}</p>
                    <div className="action-meta">
                      {item.owner && <span className="action-owner">Owner: {item.owner}</span>}
                      {item.due_date && <span className="action-due">Due: {item.due_date}</span>}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {meeting.next_steps && meeting.next_steps.length > 0 && (
          <div className="detail-section">
            <h2 className="section-title">Next Steps</h2>
            <ol className="next-steps-list">
              {meeting.next_steps.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>
          </div>
        )}
      </div>
    </div>
  );
}

export default MeetingDetail;
