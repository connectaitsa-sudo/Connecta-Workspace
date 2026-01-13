import { useEffect, useState } from 'react';
import { 
  FileText, 
  Users, 
  Clock, 
  CheckCircle, 
  Target, 
  ArrowRight,
  Download,
  Loader,
  AlertCircle
} from 'lucide-react';
import { Meeting } from '../types';
import { getMeeting, exportMeeting } from '../api';
import './MeetingResults.css';

interface MeetingResultsProps {
  meeting: Meeting | null;
  onMeetingUpdate?: (meeting: Meeting) => void;
}

function MeetingResults({ meeting, onMeetingUpdate }: MeetingResultsProps) {
  const [currentMeeting, setCurrentMeeting] = useState<Meeting | null>(meeting);
  const [isPolling, setIsPolling] = useState(false);
  const [exportingFormat, setExportingFormat] = useState<string | null>(null);

  useEffect(() => {
    setCurrentMeeting(meeting);
    
    if (meeting && ['uploaded', 'transcribing', 'processing'].includes(meeting.status)) {
      setIsPolling(true);
    }
  }, [meeting]);

  useEffect(() => {
    if (!isPolling || !currentMeeting) return;

    const pollInterval = setInterval(async () => {
      try {
        const updated = await getMeeting(currentMeeting.id);
        setCurrentMeeting(updated);
        
        if (onMeetingUpdate) {
          onMeetingUpdate(updated);
        }

        if (updated.status === 'completed' || updated.status === 'failed') {
          setIsPolling(false);
          clearInterval(pollInterval);
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [isPolling, currentMeeting, onMeetingUpdate]);

  const handleExport = async (format: 'pdf' | 'docx' | 'txt') => {
    if (!currentMeeting) return;

    setExportingFormat(format);
    try {
      const blob = await exportMeeting(currentMeeting.id, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `meeting-${currentMeeting.id}-minutes.${format}`;
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

  if (!currentMeeting) {
    return (
      <div className="results-empty">
        <FileText size={64} className="empty-icon" />
        <p className="empty-text">Upload or record audio to generate summary</p>
      </div>
    );
  }

  if (currentMeeting.status === 'failed') {
    return (
      <div className="results-error">
        <AlertCircle size={48} />
        <h3>Processing Failed</h3>
        <p>{currentMeeting.error_message || 'An error occurred while processing the meeting.'}</p>
      </div>
    );
  }

  if (['uploaded', 'transcribing', 'processing'].includes(currentMeeting.status)) {
    return (
      <div className="results-loading">
        <Loader size={48} className="spinner" />
        <h3>Processing Your Meeting...</h3>
        <p className="status-text">
          {currentMeeting.status === 'uploaded' && 'Preparing to transcribe...'}
          {currentMeeting.status === 'transcribing' && 'Transcribing audio...'}
          {currentMeeting.status === 'processing' && 'Generating meeting minutes with AI...'}
        </p>
        <div className="progress-bar">
          <div className="progress-fill"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="meeting-results">
      <div className="results-header">
        <h2 className="results-title">Meeting Minutes</h2>
        <div className="export-buttons">
          <button 
            className="export-btn"
            onClick={() => handleExport('pdf')}
            disabled={exportingFormat !== null}
          >
            <Download size={16} />
            {exportingFormat === 'pdf' ? 'Exporting...' : 'PDF'}
          </button>
          <button 
            className="export-btn"
            onClick={() => handleExport('docx')}
            disabled={exportingFormat !== null}
          >
            <Download size={16} />
            {exportingFormat === 'docx' ? 'Exporting...' : 'DOCX'}
          </button>
          <button 
            className="export-btn"
            onClick={() => handleExport('txt')}
            disabled={exportingFormat !== null}
          >
            <Download size={16} />
            {exportingFormat === 'txt' ? 'Exporting...' : 'TXT'}
          </button>
        </div>
      </div>

      {/* Summary Section */}
      <div className="minutes-section summary-section">
        <div className="section-header">
          <FileText size={20} />
          <h3>Meeting Summary</h3>
        </div>
        <p className="summary-text">{currentMeeting.summary}</p>
      </div>

      {/* Details Section */}
      <div className="details-row">
        {currentMeeting.duration_minutes && (
          <div className="detail-card">
            <Clock size={18} />
            <div>
              <div className="detail-label">Duration</div>
              <div className="detail-value">Approximately {Math.round(currentMeeting.duration_minutes)} minutes</div>
            </div>
          </div>
        )}
        
        {currentMeeting.participants && currentMeeting.participants.length > 0 && (
          <div className="detail-card">
            <Users size={18} />
            <div>
              <div className="detail-label">Participants</div>
              <div className="detail-value">{currentMeeting.participants.length}</div>
            </div>
          </div>
        )}
      </div>

      {/* Participants */}
      {currentMeeting.participants && currentMeeting.participants.length > 0 && (
        <div className="minutes-section">
          <div className="section-header">
            <Users size={20} />
            <h3>Participants</h3>
          </div>
          <div className="participants-list">
            {currentMeeting.participants.map((participant, index) => (
              <span key={index} className="participant-badge">{participant}</span>
            ))}
          </div>
        </div>
      )}

      {/* Key Discussion Points */}
      {currentMeeting.key_points && currentMeeting.key_points.length > 0 && (
        <div className="minutes-section">
          <div className="section-header">
            <Target size={20} />
            <h3>Key Discussion Points</h3>
          </div>
          <ol className="points-list">
            {currentMeeting.key_points.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ol>
        </div>
      )}

      {/* Decisions Made */}
      {currentMeeting.decisions && currentMeeting.decisions.length > 0 && (
        <div className="minutes-section decisions-section">
          <div className="section-header">
            <CheckCircle size={20} />
            <h3>Decisions Made</h3>
          </div>
          <ul className="decisions-list">
            {currentMeeting.decisions.map((decision, index) => (
              <li key={index}>
                <CheckCircle size={16} className="check-icon" />
                <span>{decision}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Action Items */}
      {currentMeeting.action_items && currentMeeting.action_items.length > 0 && (
        <div className="minutes-section action-items-section">
          <div className="section-header">
            <Target size={20} />
            <h3>Action Items</h3>
          </div>
          <div className="action-items">
            {currentMeeting.action_items.map((item, index) => (
              <div key={index} className="action-item">
                <div className="action-item-content">
                  <span className="action-description">{item.description}</span>
                  <div className="action-meta">
                    {item.owner && (
                      <span className="action-owner">
                        <Users size={14} />
                        Owner: {item.owner}
                      </span>
                    )}
                    {item.due_date && (
                      <span className="action-due">
                        <Clock size={14} />
                        Due: {item.due_date}
                      </span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Steps */}
      {currentMeeting.next_steps && currentMeeting.next_steps.length > 0 && (
        <div className="minutes-section next-steps-section">
          <div className="section-header">
            <ArrowRight size={20} />
            <h3>Next Steps</h3>
          </div>
          <ol className="next-steps-list">
            {currentMeeting.next_steps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default MeetingResults;
