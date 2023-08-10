import React, { useState, useEffect } from "react";
import { Invite } from "../SharedTypes";

interface Props {
    userId: number;
    conversationId: number;
    conversationName: string;
    invitingEmail: string;
  }

const InviteUsers: React.FC<Props> = ({ userId, conversationId, conversationName, invitingEmail }) => {
  const [email, setEmail] = useState<string>("");
  const [sentInvites, setSentInvites] = useState<Invite[]>([]);

  useEffect(() => {
    fetch(`/invitations/sent/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setSentInvites(data);
        } else {
          console.error("Error fetching sent invites:", data);
        }
      })
      .catch(err => console.error(err));
  }, [userId]);

  const handleInvite = () => {
    fetch("/invitations", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        invited_email: email, 
        inviting_user_id: userId,
        conversation_id: conversationId,
        conversation_name: conversationName,
        inviting_user_email: invitingEmail }),
    })
    .then(res => {
        if (!res.ok) {
          return res.json().then(err => { throw err });
        }
        return res.json();
      })
      .then(data => {
        setSentInvites(prev => [...prev, data]);
        setEmail("");
      })
      .catch(err => {
        console.error(err);
        alert(err.detail);
      });
  }

  return (
    <div>
      <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Invite by email" />
      <button onClick={handleInvite}>Send Invite</button>

      <h3>Invitations Sent:</h3>
      <ul>
        {sentInvites.map(invite => (
          <li key={invite.id}>
            Invited email: {invite.invited_email} <br/>
            For conversation: {invite.conversation_name} (ID: #{invite.conversation_id}) <br/>
            Status: {invite.used ? "Inactive" : "Pending"}
          </li>
        ))}
    </ul>
    </div>
  );
}

export default InviteUsers;
