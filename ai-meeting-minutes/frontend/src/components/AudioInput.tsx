import { useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, Mic, StopCircle, FileAudio } from 'lucide-react';
import { uploadAudioFile } from '../api';
import { Meeting } from '../types';
import './AudioInput.css';

interface AudioInputProps {
  onMeetingCreated: (meeting: Meeting) => void;
}

function AudioInput({ onMeetingCreated }: AudioInputProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<number | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'audio/*': ['.mp3', '.wav', '.m4a', '.ogg', '.flac'],
      'video/*': ['.mp4', '.webm', '.mov']
    },
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
      }
    }
  });

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        const file = new File([blob], `recording-${Date.now()}.webm`, { type: 'audio/webm' });
        setSelectedFile(file);
        
        stream.getTracks().forEach(track => track.stop());
        
        if (timerRef.current) {
          clearInterval(timerRef.current);
        }
        setRecordingTime(0);
      };

      mediaRecorder.start();
      setIsRecording(true);

      // Start timer
      timerRef.current = window.setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    try {
      const meeting = await uploadAudioFile(selectedFile);
      onMeetingCreated(meeting);
      setSelectedFile(null);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Failed to upload file. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-input">
      <h2 className="section-title">Input Meeting Audio</h2>

      <div className="input-methods">
        <div className="upload-section">
          <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
            <input {...getInputProps()} />
            <FileAudio size={48} className="dropzone-icon" />
            <p className="dropzone-text">Click to upload audio/video</p>
            <p className="dropzone-subtext">Supports MP3, WAV, MP4, and more</p>
          </div>
        </div>

        <div className="or-divider">OR</div>

        <div className="record-section">
          {!isRecording ? (
            <button className="record-btn" onClick={startRecording}>
              <Mic size={24} />
              <span>Start Recording</span>
            </button>
          ) : (
            <div className="recording-controls">
              <div className="recording-indicator">
                <span className="recording-dot"></span>
                <span className="recording-text">Recording... {formatTime(recordingTime)}</span>
              </div>
              <button className="stop-btn" onClick={stopRecording}>
                <StopCircle size={24} />
                <span>Stop Recording</span>
              </button>
            </div>
          )}
        </div>
      </div>

      {selectedFile && (
        <div className="selected-file">
          <div className="file-info">
            <FileAudio size={20} />
            <span className="file-name">{selectedFile.name}</span>
            <span className="file-size">
              ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
            </span>
          </div>
          <button 
            className="upload-button"
            onClick={handleUpload}
            disabled={isUploading}
          >
            {isUploading ? 'Processing...' : 'Generate Summary & Minutes'}
          </button>
        </div>
      )}
    </div>
  );
}

export default AudioInput;
