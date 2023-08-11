import "./InviteStatus.css";
import { Invite } from "../SharedTypes";
import React, { useState, useEffect } from "react";

interface Props {
  userId: number;
}

const InviteStatus: React.FC<Props> = ({ userId }) => {
  const [receivedInvites, setReceivedInvites] = useState<Invite[]>([]);
  const [sentInvites, setSentInvites] = useState<Invite[]>([]);

  useEffect(() => {
    fetch(`/invitations/sent/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setSentInvites(data);
        } else {
          console.error("Error fetching sent invites:", data);
        }
      })
      .catch((err) => console.error(err));
  }, [userId]);

  useEffect(() => {
    fetch(`/invitations/received/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setReceivedInvites(data);
        } else {
          console.error("Error fetching received invites:", data);
        }
      })
      .catch((err) => console.error(err));
  }, [userId]);

  const handleAccept = (inviteToken: string) => {
    fetch(`/invitations/${inviteToken}/accept`, { method: "PUT" })
      .then((res) => res.json())
      .then(() => {
        const updatedInvites = receivedInvites.filter(
          (invite) => invite.token !== inviteToken
        );
        setReceivedInvites(updatedInvites);
      })
      .catch((err) => console.error(err));
  };

  const handleDecline = (inviteToken: string) => {
    fetch(`/invitations/${inviteToken}/decline`, { method: "PUT" })
      .then((res) => res.json())
      .then(() => {
        const updatedInvites = receivedInvites.filter(
          (invite) => invite.token !== inviteToken
        );
        setReceivedInvites(updatedInvites);
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="received-container">
      <h3>Invitations sent by you:</h3>
      <ul>
        {sentInvites.map((invite) => (
          <li key={invite.id}>
            <span className="invite-details">Invited email:</span>{" "}
            {invite.invited_email} <br />
            <span className="invite-details">For conversation:</span>{" "}
            {invite.conversation_name} (ID: #{invite.conversation_id}) <br />
            <span className="invite-details">Status:</span>{" "}
            {invite.used ? "Inactive" : "Pending"}
          </li>
        ))}
      </ul>
      <h3>Invitations received by you:</h3>
      <ul>
        {receivedInvites.map((invite) => (
          <li key={invite.id}>
            <span className="received-details">From:</span>{" "}
            {invite.inviting_user_email} <br />
            <span className="received-details">For Conversation:</span>{" "}
            {invite.conversation_name} <br />
            <span className="received-details">Status:</span>{" "}
            {invite.used ? "Inactive" : "Pending"}
            {!invite.used && (
              <div className="invite-actions">
                <button onClick={() => handleAccept(invite.token)}>
                  Accept
                </button>
                <button onClick={() => handleDecline(invite.token)}>
                  Decline
                </button>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default InviteStatus;
