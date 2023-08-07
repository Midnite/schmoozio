import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface Conversation {
    conversation_id: number;
    conversation_name: string;
}

interface Participant {
    user_id: number;
    is_owner: boolean;
}

const ConversationDetails: React.FC<{ conversation: Conversation }> = ({ conversation }) => {
    const [participants, setParticipants] = useState<Participant[]>([]);
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
                        User ID: {participant.user_id} {participant.is_owner && '(Owner)'}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ConversationDetails;
