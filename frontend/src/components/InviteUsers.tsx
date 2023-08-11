import React, { useState } from "react";
import "./InviteUsers.css";

interface Props {
  userId: number;
  conversationId: number;
  conversationName: string;
  invitingEmail: string;
}

const InviteUsers: React.FC<Props> = ({
  userId,
  conversationId,
  conversationName,
  invitingEmail,
}) => {
  const [email, setEmail] = useState<string>("");

  const handleInvite = () => {
    fetch("/invitations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        invited_email: email,
        inviting_user_id: userId,
        conversation_id: conversationId,
        conversation_name: conversationName,
        inviting_user_email: invitingEmail,
      }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.json().then((err) => {
            throw err;
          });
        }
        return res.json();
      })
      .catch((err) => {
        console.error(err);
        alert(err.detail);
      });
  };

  return (
    <div className="invite-container">
      <h3>Invite someone to conversation {conversationName}</h3>

      <div className="invite-action">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter recipient's email address"
        />
        <button onClick={handleInvite}>Send</button>
      </div>
    </div>
  );
};

export default InviteUsers;
