import "./ChatWindow.css";
import { useAuth } from "../contexts/AuthContext";
import React, { useState, useEffect, useCallback } from "react";
import socketIOClient from "socket.io-client";

interface Props {
  onClose: () => void;
  conversationId: number;
}

const ChatWindow: React.FC<Props> = ({ onClose, conversationId }) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [content, setContent] = useState("");
  const { token, userId } = useAuth();

  const fetchMessages = useCallback(async () => {
    const response = await fetch(
      `http://localhost:8000/conversations/${conversationId}/messages`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      const text = await response.text();
      console.error("Error fetching messages:", text);
      return;
    }

    const data = await response.json();
    setMessages(data);
  }, [token, conversationId]);

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

  useEffect(() => {
    const socket = socketIOClient("http://localhost:8000");

    socket.on("connect", () => {
      console.log("Socket connected:", socket.connected);
    });

    socket.emit("join_room", conversationId);
    console.log(`Joined room: ${conversationId}`);

    socket.on("new_message", (message) => {
      console.log("Got new message: ", message);
      setMessages((prevMessages) => [...prevMessages, message]);
    });

    fetchMessages();

    socket.on("error", (error) => {
      console.error("Socket error:", error);
    });

    return () => {
      socket.emit("leave_room", conversationId);
      console.log(`Left room: ${conversationId}`);
      socket.disconnect();
    };
  }, [conversationId, fetchMessages]);

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
