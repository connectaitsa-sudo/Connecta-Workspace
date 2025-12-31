import { useState } from 'react';
import { FileText } from 'lucide-react';
import { uploadTranscript } from '../api';
import { Meeting } from '../types';
import './TranscriptInput.css';

interface TranscriptInputProps {
  onMeetingCreated: (meeting: Meeting) => void;
}

const SAMPLE_TRANSCRIPT = `John: Good morning everyone. Thanks for joining today's product review meeting. We need to discuss the Q4 roadmap and some urgent bug fixes.

Sarah: Morning! I've prepared the slides. Should we start with the roadmap or the bugs?

John: Let's tackle the bugs first since they're blocking our release. Sarah, can you give us an update?

Sarah: Sure. We have three critical bugs in the payment system. Bug #451 is causing checkout failures for about 2% of users. Bug #452 is a UI issue on mobile devices. And Bug #453 is a performance problem on the dashboard.

Mike: I've been working on Bug #451. I found the root cause - it's a race condition in our payment processing. I should have a fix ready by Friday.

Sarah: That's great news, Mike. What about the other two?`;

function TranscriptInput({ onMeetingCreated }: TranscriptInputProps) {
  const [transcript, setTranscript] = useState('');
  const [title, setTitle] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleLoadSample = () => {
    setTranscript(SAMPLE_TRANSCRIPT);
    setTitle('Product Review Meeting - Sample');
  };

  const handleSubmit = async () => {
    if (!transcript.trim()) {
      alert('Please enter or paste a transcript');
      return;
    }

    setIsProcessing(true);
    try {
      const meeting = await uploadTranscript(transcript, title || undefined);
      onMeetingCreated(meeting);
      setTranscript('');
      setTitle('');
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to process transcript. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const charCount = transcript.length;

  return (
    <div className="transcript-input">
      <h2 className="section-title">Meeting Transcript</h2>
      
      <div className="input-group">
        <label htmlFor="title">Meeting Title (Optional)</label>
        <input
          id="title"
          type="text"
          className="title-input"
          placeholder="e.g., Product Review Meeting - Q4 2024"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>

      <div className="input-group">
        <div className="textarea-header">
          <label htmlFor="transcript">Paste your meeting transcript or conversation:</label>
          <button className="load-sample-btn" onClick={handleLoadSample}>
            Load Sample Transcript
          </button>
        </div>
        <textarea
          id="transcript"
          className="transcript-textarea"
          placeholder="John: Good morning everyone. Thanks for joining today's product review meeting...

Sarah: Morning! I've prepared the slides. Should we start with the roadmap?

..."
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          rows={12}
        />
        <div className="char-count">{charCount} characters</div>
      </div>

      <div className="tip-box">
        <FileText size={16} />
        <span>
          <strong>Tip:</strong> For best results, include speaker names and clear dialogue. 
          The AI will extract action items, decisions, and key points automatically.
        </span>
      </div>

      <button 
        className="generate-button"
        onClick={handleSubmit}
        disabled={isProcessing || !transcript.trim()}
      >
        <FileText size={20} />
        <span>{isProcessing ? 'Generating...' : 'Generate Meeting Minutes'}</span>
      </button>
    </div>
  );
}

export default TranscriptInput;
