import axios from 'axios';
import { Meeting } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadAudioFile = async (file: File, title?: string): Promise<Meeting> => {
  const formData = new FormData();
  formData.append('file', file);
  if (title) {
    formData.append('title', title);
  }

  const response = await api.post<Meeting>('/api/meetings/upload-audio', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const uploadTranscript = async (transcript: string, title?: string): Promise<Meeting> => {
  const response = await api.post<Meeting>('/api/meetings/upload-transcript', {
    transcript,
  }, {
    params: { title },
  });

  return response.data;
};

export const getMeeting = async (meetingId: number): Promise<Meeting> => {
  const response = await api.get<Meeting>(`/api/meetings/${meetingId}`);
  return response.data;
};

export const listMeetings = async (): Promise<{ meetings: Meeting[]; total: number }> => {
  const response = await api.get('/api/meetings/');
  return response.data;
};

export const exportMeeting = async (meetingId: number, format: 'pdf' | 'docx' | 'txt'): Promise<Blob> => {
  const response = await api.get(`/api/meetings/${meetingId}/export/${format}`, {
    responseType: 'blob',
  });
  return response.data;
};

export const regenerateMinutes = async (meetingId: number): Promise<Meeting> => {
  const response = await api.post<Meeting>(`/api/meetings/${meetingId}/regenerate`);
  return response.data;
};

export const deleteMeeting = async (meetingId: number): Promise<void> => {
  await api.delete(`/api/meetings/${meetingId}`);
};

export default api;
