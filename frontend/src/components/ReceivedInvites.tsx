import React, { useState, useEffect } from "react";
import { Invite } from "../SharedTypes";

interface Props {
  userId: number;
}

const ReceivedInvites: React.FC<Props> = ({ userId }) => {
  const [receivedInvites, setReceivedInvites] = useState<Invite[]>([]);

  useEffect(() => {
    fetch(`/invitations/received/${userId}`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setReceivedInvites(data);
        } else {
          console.error("Error fetching sent invites:", data);
        }
      })
      .catch(err => console.error(err));
  }, [userId]);

  const handleAccept = (inviteId: number) => {
    fetch(`/invitations/${inviteId}/accept`, { method: 'PUT' })
      .then(res => res.json())
      .then(() => {
        const updatedInvites = receivedInvites.filter(invite => invite.id !== inviteId);
        setReceivedInvites(updatedInvites);
      })
      .catch(err => console.error(err));
  }

  const handleDecline = (inviteId: number) => {
    fetch(`/invitations/${inviteId}/decline`, { method: 'PUT' })
      .then(res => res.json())
      .then(() => {
        const updatedInvites = receivedInvites.filter(invite => invite.id !== inviteId);
        setReceivedInvites(updatedInvites);
      })
      .catch(err => console.error(err));
  }

  return (
    <div>
      <h3>Invitations Received:</h3>
      <ul>
        {receivedInvites.map(invite => (
          <li key={invite.id}>
            From: {invite.inviting_user_email}  <br/>
            For Conversation: {invite.conversation_name}  <br/>
            <button onClick={() => handleAccept(invite.id)}>Accept</button>
            <button onClick={() => handleDecline(invite.id)}>Decline</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReceivedInvites;
