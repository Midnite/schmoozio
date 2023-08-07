import React, { useState } from 'react';

interface Props {
  onCreate: (data: any) => void;
}

function CreateConversation({ onCreate }: Props) {
    const [name, setName] = useState("");

    const handleSubmit = async () => {
        const response = await fetch("http://localhost:8000/conversations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer YOUR_ACCESS_TOKEN" // Replace this with the user's token
            },
            body: JSON.stringify({ conversation_name: name })
        });

        const data = await response.json();
        onCreate(data);
        setName("");
    };

    return (
        <div>
            <input 
                type="text" 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="Enter conversation name" 
            />
            <button onClick={handleSubmit}>Create Conversation</button>
        </div>
    );
}

export default CreateConversation;