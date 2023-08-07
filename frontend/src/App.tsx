import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css';

const App: React.FC = () => {
    const [loggedInUser, setLoggedInUser] = useState<string | null>(null);

    return (
        <div className="container">
                <h2>Login</h2>
                {loggedInUser ? `Welcome, ${loggedInUser}, you've logged in successfully.` : <LoginForm setLoggedInUser={setLoggedInUser} />}

                <h2>Register</h2>
                <RegisterForm />
        </div>
    );
}

export default App;
