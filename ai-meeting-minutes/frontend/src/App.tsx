import { useState } from 'react';
import Header from './components/Header';
import AudioInput from './components/AudioInput';
import TranscriptInput from './components/TranscriptInput';
import MeetingResults from './components/MeetingResults';
import { Meeting } from './types';
import './App.css';

function App() {
  const [currentMeeting, setCurrentMeeting] = useState<Meeting | null>(null);
  const [inputMode, setInputMode] = useState<'audio' | 'transcript'>('audio');

  const handleMeetingCreated = (meeting: Meeting) => {
    setCurrentMeeting(meeting);
  };

  const handleMeetingUpdate = (meeting: Meeting) => {
    setCurrentMeeting(meeting);
  };

  return (
    <div className="app">
      <Header />
      
      <div className="main-container">
        <div className="input-section">
          <div className="mode-selector">
            <button
              className={`mode-btn ${inputMode === 'audio' ? 'active' : ''}`}
              onClick={() => setInputMode('audio')}
            >
              Audio/Video Upload
            </button>
            <button
              className={`mode-btn ${inputMode === 'transcript' ? 'active' : ''}`}
              onClick={() => setInputMode('transcript')}
            >
              Transcript Text
            </button>
          </div>

          {inputMode === 'audio' ? (
            <AudioInput onMeetingCreated={handleMeetingCreated} />
          ) : (
            <TranscriptInput onMeetingCreated={handleMeetingCreated} />
          )}
        </div>

        <div className="results-section">
          <MeetingResults 
            meeting={currentMeeting} 
            onMeetingUpdate={handleMeetingUpdate}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
