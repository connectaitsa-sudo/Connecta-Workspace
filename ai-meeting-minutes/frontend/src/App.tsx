import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import NewMeeting from './components/NewMeeting';
import MeetingDetail from './components/MeetingDetail';
import Integrations from './components/Integrations';
import Settings from './components/Settings';
import { Meeting } from './types';
import { listMeetings } from './api';
import './App.css';

type View = 'dashboard' | 'new-meeting' | 'meeting-detail' | 'integrations' | 'settings';

function App() {
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [selectedMeeting, setSelectedMeeting] = useState<Meeting | null>(null);
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMeetings();
  }, []);

  const loadMeetings = async () => {
    try {
      setLoading(true);
      const data = await listMeetings();
      setMeetings(data.meetings);
    } catch (error) {
      console.error('Failed to load meetings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewMeeting = (meeting: Meeting) => {
    setSelectedMeeting(meeting);
    setCurrentView('meeting-detail');
  };

  const handleMeetingCreated = (meeting: Meeting) => {
    setMeetings(prev => [meeting, ...prev]);
    setSelectedMeeting(meeting);
    setCurrentView('meeting-detail');
  };

  const handleMeetingUpdated = (meeting: Meeting) => {
    setMeetings(prev => prev.map(m => m.id === meeting.id ? meeting : m));
    if (selectedMeeting?.id === meeting.id) {
      setSelectedMeeting(meeting);
    }
  };

  const handleMeetingDeleted = (meetingId: number) => {
    setMeetings(prev => prev.filter(m => m.id !== meetingId));
    if (selectedMeeting?.id === meetingId) {
      setSelectedMeeting(null);
      setCurrentView('dashboard');
    }
  };

  return (
    <div className="app">
      <Sidebar 
        currentView={currentView}
        onNavigate={setCurrentView}
      />
      
      <main className="main-content">
        {currentView === 'dashboard' && (
          <Dashboard
            meetings={meetings}
            loading={loading}
            onViewMeeting={handleViewMeeting}
            onRefresh={loadMeetings}
          />
        )}

        {currentView === 'new-meeting' && (
          <NewMeeting
            onMeetingCreated={handleMeetingCreated}
            onBack={() => setCurrentView('dashboard')}
          />
        )}

        {currentView === 'meeting-detail' && selectedMeeting && (
          <MeetingDetail
            meeting={selectedMeeting}
            onBack={() => setCurrentView('dashboard')}
            onMeetingUpdated={handleMeetingUpdated}
            onMeetingDeleted={handleMeetingDeleted}
          />
        )}

        {currentView === 'integrations' && (
          <Integrations />
        )}

        {currentView === 'settings' && (
          <Settings />
        )}
      </main>
    </div>
  );
}

export default App;
