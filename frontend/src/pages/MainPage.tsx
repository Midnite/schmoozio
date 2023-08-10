import React from 'react';
import ConversationCreator from '../components/ConversationCreator';
import { User } from '../SharedTypes';

const MainPage: React.FC<{ user: User }> = ({ user }) => {
  return (
    <div>
      <h2>Welcome, {user.username}!</h2>
      <ConversationCreator user={user}/>
    </div>
  );
}

export default MainPage;
