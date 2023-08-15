import "./ChatWindow.css";
import { useAuth } from "../contexts/AuthContext";
import React, { useState, useEffect } from "react";

interface Props {
  onClose: () => void;
  conversationId: number;
}

const ChatWindow: React.FC<Props> = ({ onClose, conversationId }) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [content, setContent] = useState("");
  const { token, userId } = useAuth();

  useEffect(() => {
    const socket = new WebSocket(`ws://localhost:8000/ws/${conversationId}`);

    socket.onopen = () => {
      console.log("WebSocket connection opened!");
    };

    // socket.onmessage = (event) => {
    //   const message = JSON.parse(event.data);
    //   setMessages((prevMessages) => [...prevMessages, message]);
    // };

    socket.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      const message = JSON.parse(event.data);
      setMessages((prevMessages) => [...prevMessages, message]);
    };

    socket.onerror = (event) => {
      console.error("WebSocket Error", event);
    };

    socket.onclose = (event) => {
      console.warn("WebSocket Closed", event);
    };

    return () => {
      socket.close();
    };
  }, [conversationId]);

  const sendMessage = async () => {
    const response = await fetch(
      `http://localhost:8000/conversations/${conversationId}/messages`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          user_id: userId,
          content: content,
        }),
      }
    );

    if (response.ok) {
      setContent("");
    } else {
      console.error("Error sending message:", await response.text());
    }
  };

  return (
    <div className="chat-window">
      <h3>Schmoozio Chat</h3>
      <div className="messages">
        {messages.length === 0 && <div>No messages yet!</div>}
        {messages.map((message) => (
          <div key={message.message_id}>
            <span>{message.user ? message.user.username : "Unknown"}: </span>
            {message.content}
          </div>
        ))}
      </div>
      <div>
        <input
          placeholder="Type your message"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <div className="message-input">
          <button onClick={sendMessage}>Send</button>
          <button onClick={onClose}>Close Chat</button>
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
