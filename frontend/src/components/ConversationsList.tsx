import { Conversation } from '../SharedTypes';

interface ConversationsListProps {
  conversations: Conversation[];
  onSelect: (conv: Conversation) => void;
}

function ConversationsList({ conversations, onSelect }: ConversationsListProps) {
    return (
        <ul>
            {conversations.map(conv => (
                <li key={conv.conversation_id} onClick={() => onSelect(conv)}>
                    {conv.conversation_name}
                </li>
            ))}
        </ul>
    );
}

export default ConversationsList;