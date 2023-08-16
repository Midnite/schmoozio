import { Conversation } from "../SharedTypes";

interface ConversationsListProps {
  conversations: Conversation[];
  selectedConversation: Conversation | null;
  onSelect: (conv: Conversation) => void;
}

function ConversationsList({
  conversations,
  selectedConversation,
  onSelect,
}: ConversationsListProps) {
  return (
    <ul>
      {conversations.map((conv) => (
        <li
          key={conv.conversation_id}
          onClick={() => onSelect(conv)}
          className={`conversation-item ${
            selectedConversation &&
            selectedConversation.conversation_id === conv.conversation_id
              ? "selected-conversation-item"
              : ""
          }`}
        >
          {conv.conversation_name}
        </li>
      ))}
    </ul>
  );
}

export default ConversationsList;
