import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base, User, Conversation, Participant, Message

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.db = TestingSessionLocal()
    
    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_create_user(self):
        response = self.client.post("/users/", json={"username": "test_user", "email": "test@example.com", "password": "password"})
        assert response.status_code == 200
        user_id = response.json()["user_id"]
        user = self.db.query(User).filter(User.user_id == user_id).first()
        assert user is not None, "User should not be None"
        assert user.email == "test@example.com", f"Expected email 'test@example.com', but got {user.email}"

    def test_create_conversation(self):
        response = self.client.post("/conversations/", json={"conversation_name": "test_conversation"})
        assert response.status_code == 200, "Response should be 200"
        conversation_id = response.json()["conversation_id"]
        conversation_name = response.json()["conversation_name"]
        assert conversation_name == "test_conversation", f"Expected conversation_name 'test_conversation', but got {conversation_name}"
        db_conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        assert db_conversation is not None, "Conversation should not be None"
        assert db_conversation.conversation_name == "test_conversation", f"Expected conversation_name 'test_conversation', but got {db_conversation.conversation_name}"
        assert db_conversation.created_at is not None, "'created_at' should not be None"

    def test_create_message(self):
        user_response = self.client.post("/users/", json={"username": "test_user", "email": "test@example.com", "password": "password"})
        user_id = user_response.json()["user_id"]
 
        conv_response = self.client.post("/conversations/", json={"conversation_name": "test_conversation"})
        conv_id = conv_response.json()["conversation_id"]
        response = self.client.post(
            f"/conversations/{conv_id}/messages", 
            json={"user_id": user_id, "content": "Test content", "conversation_id": conv_id}
        )
        
        assert response.status_code == 200
        message_id = response.json()["message_id"]
        message = self.db.query(Message).filter(Message.message_id == message_id).first()

        assert message is not None, "Message should not be None"
        assert message.content == "Test content", f"Expected content 'Test content', but got {message.content}"
        assert message.user_id == user_id, f"Expected user_id '{user_id}', but got {message.user_id}"
        assert message.conversation_id == conv_id, f"Expected conversation_id '{conv_id}', but got {message.conversation_id}"

    def test_create_participant(self):

        response = self.client.post("/conversations/", json={"conversation_name": "test_conversation"})
        assert response.status_code == 200
        conversation_id = response.json()["conversation_id"]
        
        user_response = self.client.post("/users/", json={"username": "test_user", "email": "test@example.com", "password": "password"})
        assert user_response.status_code == 200
        user_id = user_response.json()["user_id"]

        participant_response = self.client.post(f"/conversations/{conversation_id}/participants", json={"user_id": user_id, "is_owner": True})        
        assert participant_response.status_code == 200
        participant_data = participant_response.json()
        assert participant_data["user_id"] == user_id
        assert participant_data["is_owner"] == True
        assert "id" in participant_data

if __name__ == "__main__":
    unittest.main()
