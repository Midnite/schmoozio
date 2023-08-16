import "./ConversationDetails.css";
import { useAuth } from "../contexts/AuthContext";
import { User, Conversation } from "../SharedTypes";
import ChatWindow from "./ChatWindow";
import InviteUsers from "./InviteUsers";
import React, { useState, useEffect } from "react";

interface ConversationDetailsProps {
  conversation: Conversation;
  user: User;
}

interface Participant {
  participant_id: number;
  username: string;
  is_owner: boolean;
}

const ConversationDetails: React.FC<ConversationDetailsProps> = ({
  conversation,
  user,
}) => {
  const [participants, setParticipants] = useState<Participant[]>([]);
  const [chatOpen, setChatOpen] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    if (token) {
      fetch(
        `http://localhost:8000/conversations/${conversation.conversation_id}/participants`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
        .then((response) => response.json())
        .then(setParticipants)
        .catch((error) => console.error("Error fetching participants:", error));
    }
  }, [conversation, token]);

  return (
    <div className="details-container">
      <h3 className="selected-conversation">
        Selected conversation: {conversation.conversation_name}
      </h3>
      <h4>Participants in conversation:</h4>
      <ul className="participant-list">
        {participants.map((participant) => (
          <li key={participant.participant_id} className="participant">
            User: {participant.username}
            {participant.is_owner && (
              <span className="participant-owner">(Owner)</span>
            )}
          </li>
        ))}
      </ul>
      {!chatOpen && (
        <button className="open-chat-btn" onClick={() => setChatOpen(true)}>
          Open Chat
        </button>
      )}
      {chatOpen && (
        <ChatWindow
          conversationId={conversation.conversation_id}
          onClose={() => setChatOpen(false)}
        />
      )}

      <div className="invite-section">
        <InviteUsers
          userId={user.user_id}
          conversationId={conversation.conversation_id}
          conversationName={conversation.conversation_name}
          invitingEmail={user.email}
        />
      </div>
    </div>
  );
};

export default ConversationDetails;
