import React, { useState, useEffect } from 'react';
import { useAuth } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css';
import ConversationCreator from './components/ConversationCreator';

const App: React.FC = () => {
    const [loggedInUser, setLoggedInUser] = useState<string | null>(() => localStorage.getItem('loggedInUser'));

    useEffect(() => {
        localStorage.setItem('loggedInUser', loggedInUser || '');
    }, [loggedInUser]);

    const { logout: originalLogout } = useAuth();

    const logout = () => {
        setLoggedInUser(null);
        originalLogout();
    };

    return (
        <div className="container">
            {loggedInUser ? 
                <div>
                    <h2>Welcome, {loggedInUser}!</h2> 
                    <ConversationCreator />
                    <button onClick={logout}>Logout</button>
                </div>
                :
                <>
                    <h2>Login</h2>
                    <LoginForm setLoggedInUser={setLoggedInUser} />
                    
                    <h2>Register</h2>
                    <RegisterForm />
                </>
            }
        </div>
    );
}

export default App;
