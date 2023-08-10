import React, { useState, FormEvent } from 'react';
import { useAuth } from '../contexts/AuthContext';

interface LoginFormProps {
    setLoggedInUser: (user: string | null) => void;
}

const LoginForm: React.FC<LoginFormProps> = ({ setLoggedInUser }) => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const { setToken, setUserId } = useAuth();

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setErrorMessage(null);
        
        const response = await fetch('http://localhost:8000/users/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
    
        const data = await response.json();

        
        if (response.status === 200) {
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('userId', data.user_id.toString());  // Add this
            alert('Logged in successfully');
            setLoggedInUser(username);
            setToken(data.access_token);
            setUserId(data.user_id.toString());  // Add this
        } else {
            setErrorMessage(data.detail || 'Error logging in');
        }
    };
    

    return (
        <div className="form-container">
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <form onSubmit={handleSubmit}>
                <input 
                    value={username} 
                    onChange={e => setUsername(e.target.value)} 
                    placeholder="Username" 
                    required 
                />
                <input 
                    type="password" 
                    value={password} 
                    onChange={e => setPassword(e.target.value)} 
                    placeholder="Password" 
                    required 
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginForm;
