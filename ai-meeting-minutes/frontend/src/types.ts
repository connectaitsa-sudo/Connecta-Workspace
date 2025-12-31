export interface ActionItem {
  description: string;
  owner?: string;
  due_date?: string;
}

export interface Meeting {
  id: number;
  title?: string;
  source_type: string;
  status: string;
  transcript?: string;
  duration_minutes?: number;
  participants?: string[];
  summary?: string;
  key_points?: string[];
  decisions?: string[];
  action_items?: ActionItem[];
  next_steps?: string[];
  created_at: string;
  updated_at: string;
  error_message?: string;
}

export interface MeetingMinutes {
  summary: string;
  duration_minutes?: number;
  participants: string[];
  key_points: string[];
  decisions: string[];
  action_items: ActionItem[];
  next_steps: string[];
}
