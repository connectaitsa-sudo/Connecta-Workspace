import { useState, useRef } from 'react';
import { ArrowLeft, Upload, Mic, StopCircle, FileText, Loader } from 'lucide-react';
import { useDropzone } from 'react-dropzone';
import { uploadAudioFile, uploadTranscript } from '../api';
import { Meeting } from '../types';
import './NewMeeting.css';

interface NewMeetingProps {
  onMeetingCreated: (meeting: Meeting) => void;
  onBack: () => void;
}

function NewMeeting({ onMeetingCreated, onBack }: NewMeetingProps) {
  const [inputMode, setInputMode] = useState<'upload' | 'record' | 'transcript'>('upload');
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState('');
  const [title, setTitle] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'audio/*': ['.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac'],
      'video/*': ['.mp4', '.webm', '.mov', '.avi']
    },
    multiple: false,
    maxSize: 500 * 1024 * 1024, // 500MB
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
        setError(null);
      }
    },
    onDropRejected: (fileRejections) => {
      const error = fileRejections[0]?.errors[0];
      if (error?.code === 'file-too-large') {
        setError('File is too large. Maximum size is 500MB.');
      } else {
        setError('Invalid file type. Please upload an audio or video file.');
      }
    }
  });

  const startRecording = async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        }
      });

      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });

      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const file = new File([blob], `recording-${Date.now()}.webm`, { 
          type: 'audio/webm' 
        });
        setSelectedFile(file);
        stream.getTracks().forEach(track => track.stop());
        
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
        setRecordingTime(0);
      };

      mediaRecorder.start(100); // Collect data every 100ms
      setIsRecording(true);

      // Start timer
      timerRef.current = window.setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error: any) {
      console.error('Recording error:', error);
      if (error.name === 'NotAllowedError') {
        setError('Microphone access denied. Please allow microphone access and try again.');
      } else if (error.name === 'NotFoundError') {
        setError('No microphone found. Please connect a microphone and try again.');
      } else {
        setError('Failed to start recording. Please check your microphone settings.');
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const meeting = await uploadAudioFile(selectedFile, title || undefined);
      onMeetingCreated(meeting);
    } catch (error: any) {
      console.error('Upload error:', error);
      setError(error.response?.data?.detail || 'Failed to upload file. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTranscriptSubmit = async () => {
    if (!transcript.trim()) {
      setError('Please enter a transcript.');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const meeting = await uploadTranscript(transcript, title || undefined);
      onMeetingCreated(meeting);
    } catch (error: any) {
      console.error('Upload error:', error);
      setError(error.response?.data?.detail || 'Failed to process transcript. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="new-meeting">
      <div className="new-meeting-header">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} />
          Back
        </button>
        <div>
          <h1 className="page-title">Create New Meeting</h1>
          <p className="page-subtitle">Upload audio, record, or paste a transcript</p>
        </div>
      </div>

      <div className="new-meeting-content">
        {/* Title Input */}
        <div className="input-group">
          <label htmlFor="title">Meeting Title (Optional)</label>
          <input
            id="title"
            type="text"
            className="input"
            placeholder="e.g., Q4 Planning Meeting"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        {/* Mode Selector */}
        <div className="mode-tabs">
          <button
            className={`mode-tab ${inputMode === 'upload' ? 'active' : ''}`}
            onClick={() => setInputMode('upload')}
          >
            <Upload size={18} />
            Upload File
          </button>
          <button
            className={`mode-tab ${inputMode === 'record' ? 'active' : ''}`}
            onClick={() => setInputMode('record')}
          >
            <Mic size={18} />
            Record Audio
          </button>
          <button
            className={`mode-tab ${inputMode === 'transcript' ? 'active' : ''}`}
            onClick={() => setInputMode('transcript')}
          >
            <FileText size={18} />
            Paste Transcript
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="alert alert-error">
            {error}
          </div>
        )}

        {/* Upload Mode */}
        {inputMode === 'upload' && (
          <div className="upload-section">
            <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
              <input {...getInputProps()} />
              <Upload size={48} className="dropzone-icon" />
              <p className="dropzone-text">
                {isDragActive ? 'Drop your file here' : 'Drag & drop your audio/video file'}
              </p>
              <p className="dropzone-subtext">or click to browse</p>
              <p className="dropzone-formats">
                Supports: MP3, WAV, MP4, M4A, WebM, OGG • Max 500MB
              </p>
            </div>

            {selectedFile && (
              <div className="selected-file">
                <div className="file-info">
                  <FileText size={24} />
                  <div>
                    <p className="file-name">{selectedFile.name}</p>
                    <p className="file-size">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  className="btn btn-primary btn-lg"
                  onClick={handleUpload}
                  disabled={isProcessing}
                >
                  {isProcessing ? (
                    <>
                      <Loader size={18} className="animate-spin" />
                      Processing...
                    </>
                  ) : (
                    'Generate Minutes'
                  )}
                </button>
              </div>
            )}
          </div>
        )}

        {/* Record Mode */}
        {inputMode === 'record' && (
          <div className="record-section">
            {!isRecording && !selectedFile ? (
              <div className="record-start">
                <button className="btn-record" onClick={startRecording}>
                  <Mic size={32} />
                  <span>Start Recording</span>
                </button>
                <p className="record-hint">
                  Click to start recording your meeting
                </p>
              </div>
            ) : isRecording ? (
              <div className="recording-active">
                <div className="recording-indicator">
                  <span className="recording-dot"></span>
                  <span className="recording-time">{formatTime(recordingTime)}</span>
                </div>
                <p className="recording-text">Recording in progress...</p>
                <button className="btn-stop" onClick={stopRecording}>
                  <StopCircle size={24} />
                  Stop Recording
                </button>
              </div>
            ) : (
              <div className="selected-file">
                <div className="file-info">
                  <FileText size={24} />
                  <div>
                    <p className="file-name">{selectedFile.name}</p>
                    <p className="file-size">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <div className="file-actions">
                  <button
                    className="btn btn-secondary"
                    onClick={() => setSelectedFile(null)}
                  >
                    Record Again
                  </button>
                  <button
                    className="btn btn-primary btn-lg"
                    onClick={handleUpload}
                    disabled={isProcessing}
                  >
                    {isProcessing ? (
                      <>
                        <Loader size={18} className="animate-spin" />
                        Processing...
                      </>
                    ) : (
                      'Generate Minutes'
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Transcript Mode */}
        {inputMode === 'transcript' && (
          <div className="transcript-section">
            <textarea
              className="transcript-input"
              placeholder="Paste your meeting transcript here...

Example:
John: Good morning team. Let's discuss the Q4 roadmap.
Sarah: I've prepared three proposals...
"
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              rows={15}
            />
            <div className="transcript-footer">
              <p className="char-count">{transcript.length} characters</p>
              <button
                className="btn btn-primary btn-lg"
                onClick={handleTranscriptSubmit}
                disabled={isProcessing || !transcript.trim()}
              >
                {isProcessing ? (
                  <>
                    <Loader size={18} className="animate-spin" />
                    Processing...
                  </>
                ) : (
                  'Generate Minutes'
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default NewMeeting;
