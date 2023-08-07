import React from 'react';

interface Conversation {
  id: number;
  conversation_name: string;
}

interface ConversationsListProps {
  conversations: Conversation[];
  onSelect: (conv: Conversation) => void;
}

function ConversationsList({ conversations, onSelect }: ConversationsListProps) {
    return (
        <ul>
            {conversations.map(conv => (
                <li key={conv.id} onClick={() => onSelect(conv)}>
                    {conv.conversation_name}
                </li>
            ))}
        </ul>
    );
}

export default ConversationsList;