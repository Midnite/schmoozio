import "./InviteStatus.css";
import { Invite } from "../SharedTypes";
import React, { useState, useEffect } from "react";

interface Props {
  userId: number;
}

const InviteStatus: React.FC<Props> = ({ userId }) => {
  const [receivedInvites, setReceivedInvites] = useState<Invite[]>([]);
  const [sentInvites, setSentInvites] = useState<Invite[]>([]);
  const [isSentListOpen, setSentListOpen] = useState(false);
  const [isReceivedListOpen, setReceivedListOpen] = useState(false);

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
    <div
      className={
        sentInvites.length > 0 || receivedInvites.length > 0
          ? "received-container"
          : "hidden-section"
      }
    >
      {sentInvites.length > 0 && (
        <>
          <h3 onClick={() => setSentListOpen(!isSentListOpen)}>
            Invitations sent by you:
            <span className={`arrow-icon ${isSentListOpen ? "open" : ""}`}>
              ▼
            </span>
          </h3>
          {isSentListOpen && (
            <ul>
              {sentInvites.map((invite) => (
                <li key={invite.id}>
                  <span className="invite-details">Invited email: </span>
                  {invite.invited_email} <br />
                  <span className="invite-details">For conversation: </span>
                  {invite.conversation_name} (ID: #{invite.conversation_id}){" "}
                  <br />
                  <span className="invite-details">Status: </span>
                  {invite.used ? "Inactive / Complete" : "Pending"}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
      {receivedInvites.length > 0 && (
        <>
          <h3 onClick={() => setReceivedListOpen(!isReceivedListOpen)}>
            Invitations received by you:
            <span className={`arrow-icon ${isReceivedListOpen ? "open" : ""}`}>
              ▼
            </span>
          </h3>

          {isReceivedListOpen && (
            <ul>
              {receivedInvites.map((invite) => (
                <li key={invite.id}>
                  <span className="received-details">From:</span>
                  {invite.inviting_user_email} <br />
                  <span className="received-details">For Conversation:</span>
                  {invite.conversation_name} <br />
                  <span className="received-details">Status:</span>
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
          )}
        </>
      )}
    </div>
  );
};

export default InviteStatus;
