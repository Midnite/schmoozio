import "./ConversationCreator.css";
import { useAuth } from "../contexts/AuthContext";
import { User, Conversation } from "../SharedTypes";
import ConversationDetails from "./ConversationDetails";
import React, { useState, FormEvent, useEffect } from "react";
import ConversationsList from "./ConversationsList";
interface ConversationCreatorProps {
  user: User;
}

const ConversationCreator: React.FC<ConversationCreatorProps> = ({ user }) => {
  const [conversationName, setConversationName] = useState<string>("");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] =
    useState<Conversation | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const { token } = useAuth();

  useEffect(() => {
    if (token) {
      fetch("http://localhost:8000/users/conversations", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (Array.isArray(data)) {
            setConversations(data);
          } else {
            console.error("Expected an array from the server, but got:", data);
          }
        })
        .catch((error) =>
          console.error("Error fetching conversations:", error)
        );
    }
  }, [token]);

  const handleCreateConversation = async (e: FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (token) {
      const response = await fetch("http://localhost:8000/conversations", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ conversation_name: conversationName }),
      });

      const data = await response.json();
      if (response.ok) {
        setConversations((prevConversations) => [...prevConversations, data]);
      } else {
        setErrorMessage(data.detail || "Error creating conversation");
      }
    }
    setConversationName("");
  };

  return (
    <div className="form-container">
      <h2 className="conversation-heading">Create a conversation</h2>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <form onSubmit={handleCreateConversation}>
        <input
          className="conversation-input"
          value={conversationName}
          onChange={(e) => setConversationName(e.target.value)}
          placeholder="Conversation Name"
          required
        />
        <button className="conversation-button" type="submit">
          Create Conversation
        </button>
      </form>

      {conversations.length > 0 ? (
        <div>
          <h2 className="conversation-heading">Your Conversations</h2>
          <ConversationsList
            conversations={conversations}
            selectedConversation={selectedConversation}
            onSelect={setSelectedConversation}
          />
        </div>
      ) : (
        <h3>No conversations yet</h3>
      )}

      {selectedConversation && (
        <ConversationDetails conversation={selectedConversation} user={user} />
      )}
    </div>
  );
};

export default ConversationCreator;
