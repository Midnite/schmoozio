import React, { useState, useEffect } from 'react';
import ChatWindow from './ChatWindow';
import { useAuth } from '../contexts/AuthContext';
import InviteUsers from "./InviteUsers";
import ReceivedInvites from "./ReceivedInvites";
import { User, Conversation } from '../SharedTypes';

interface ConversationDetailsProps {
    conversation: Conversation;
    user: User;
}

interface Participant {
    user_id: number;
    username: string;
    is_owner: boolean;
}

const ConversationDetails: React.FC<ConversationDetailsProps> = ({ conversation, user }) => {    const [participants, setParticipants] = useState<Participant[]>([]);
    const [chatOpen, setChatOpen] = useState(false);
    const { token } = useAuth();

    useEffect(() => {
        if (token) {
            fetch(`http://localhost:8000/conversations/${conversation.conversation_id}/participants`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(setParticipants)
            .catch(error => console.error('Error fetching participants:', error));
        }
    }, [conversation, token]);

    return (
        <div>
            <h3>Selected: {conversation.conversation_name}</h3>
            <ul>
                {participants.map(participant => (
                    <li key={participant.user_id}>
                        Username: {participant.username} {participant.is_owner && '(Owner)'}
                    </li>
                ))}
            </ul>
            {!chatOpen && <button onClick={() => setChatOpen(true)}>Open Chat</button>}
            {chatOpen && <ChatWindow conversationId={conversation.conversation_id} onClose={() => setChatOpen(false)} />}        
                <div>
                    <InviteUsers 
                    userId={user.user_id} 
                    conversationId={conversation.conversation_id}
                    conversationName={conversation.conversation_name} 
                    invitingEmail={user.email}/>
                    <ReceivedInvites userId={user.user_id} />
                </div>
            </div>
    );
};

export default ConversationDetails;
