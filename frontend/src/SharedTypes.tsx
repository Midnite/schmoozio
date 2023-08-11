export interface User {
  user_id: number;
  username: string;
  email: string;
}

export interface Conversation {
  conversation_id: number;
  conversation_name: string;
}

export interface Invite {
  id: number;
  invited_email: string;
  used: boolean;
  conversation_id: number;
  inviting_user_email: string;
  conversation_name: string;
  token: string;
}
