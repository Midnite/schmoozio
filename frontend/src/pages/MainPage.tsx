import { User } from "../SharedTypes";
import ConversationCreator from "../components/ConversationCreator";
import InviteStatus from "../components/InviteStatus";
import React from "react";

const MainPage: React.FC<{ user: User }> = ({ user }) => {
  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <ConversationCreator user={user} />
      <InviteStatus userId={user.user_id} />
    </div>
  );
};

export default MainPage;
