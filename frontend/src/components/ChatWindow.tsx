import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './ChatWindow.css';

interface Props {
    onClose: () => void;
    conversationId: number;
}

const ChatWindow: React.FC<Props> = ({ onClose, conversationId }) => {
    const [messages, setMessages] = useState<any[]>([]);
    const [content, setContent] = useState('');
    const { token, userId } = useAuth();
    // const auth = useAuth();

    const fetchMessages = useCallback(async () => {
            const response = await fetch(`http://localhost:8000/conversations/${conversationId}/messages`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
    
        if (!response.ok) {
            const text = await response.text();
            console.error("Error fetching messages:", text);
            return;
        }
    
        const data = await response.json();
        setMessages(data);
    }, [token, conversationId]);

    useEffect(() => {
        fetchMessages();
    }, [fetchMessages]);
    

    const sendMessage = async () => {
        const response = await fetch(`http://localhost:8000/conversations/${conversationId}/messages`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                user_id: userId,
                content: content
            })
        });
        if (response.ok) {
            const newMessage = await response.json();
            setMessages(prevMessages => [...prevMessages, newMessage]);
            setContent('');
        } else {
            console.error("Error sending message:", await response.text());
        }
    };
    

    return (
        <div className="chat-window">
            <h3>Schmoozio Chat</h3>
            <div className="messages">
                {messages.length === 0 && <div>No messages yet!</div>}
                {messages.map(message => (
                    <div key={message.message_id}>
                    <span>{message.user ? message.user.username : 'Unknown'}: </span>
                    {message.content}
                    </div>
                ))}
            </div>
            <div >
                <input placeholder='Type your message' value={content} onChange={e => setContent(e.target.value)} />
                <div className="message-input">
                    <button onClick={sendMessage}>Send</button>
                    <button onClick={onClose}>Close Chat</button>
                </div>
            </div>
        </div>
    );
};

export default ChatWindow;
