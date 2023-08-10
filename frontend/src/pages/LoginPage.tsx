import React from 'react';
import LoginForm from '../components/LoginForm';

interface LoginPageProps {
    setLoggedInUser: (user: string | null) => void;
  }

  const LoginPage: React.FC<LoginPageProps> = ({ setLoggedInUser }) => {
    return (
    <div>
      <h2>Login</h2>
      <LoginForm setLoggedInUser={setLoggedInUser} />
    </div>
  );
}

export default LoginPage;
