import React, { useState, FormEvent, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ConversationDetails from './ConversationDetails';
import { User, Conversation } from '../SharedTypes';

interface ConversationCreatorProps {
    user: User
}

const ConversationCreator: React.FC<ConversationCreatorProps> = ({ user }) => {    
    const [conversationName, setConversationName] = useState<string>('');
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const { token } = useAuth();

    useEffect(() => {
        if (token) {
            fetch('http://localhost:8000/users/conversations', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => response.json())
            .then(data => {
                if (Array.isArray(data)) {
                    setConversations(data);
                } else {
                    console.error('Expected an array from the server, but got:', data);
                }
            })
            .catch(error => console.error('Error fetching conversations:', error));
        }
    }, [token]);

    const handleCreateConversation = async (e: FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);

        if (token) {
            const response = await fetch('http://localhost:8000/conversations', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ conversation_name: conversationName }),
            });
            
            const data = await response.json();
            if (response.ok) {
                setConversations(prevConversations => [...prevConversations, data]);
            } else {
                setErrorMessage(data.detail || 'Error creating conversation');
            }
        }
    };

    return (
        <div className="form-container">
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <form onSubmit={handleCreateConversation}>
                <input 
                    value={conversationName} 
                    onChange={e => setConversationName(e.target.value)} 
                    placeholder="Conversation Name"
                    required
                />
                <button type="submit">Create Conversation</button>
            </form>
            
            <div>
                {conversations.length > 0 ? (
                    <div>
                        <h2>Your Conversations</h2>
                        {conversations.map(conversation => (
                            <div 
                                key={conversation.conversation_id} 
                                onClick={() => setSelectedConversation(conversation)}
                                style={{ cursor: 'pointer' }}
                            >
                                {conversation.conversation_name} - 
                                 #{conversation.conversation_id}
                            </div>
                        ))}
                    </div>
                ) : (
                    <h3>No conversations yet</h3>
                )}
            </div>

            {selectedConversation && <ConversationDetails conversation={selectedConversation} user={user}/>}
        </div>
    );
};

export default ConversationCreator;
