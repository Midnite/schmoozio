import React from "react";
import LoginForm from "../components/LoginForm";
import { Link } from "react-router-dom";

interface LoginPageProps {
  setLoggedInUser: (user: string | null) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ setLoggedInUser }) => {
  return (
    <div>
      <h2>Login</h2>
      <LoginForm setLoggedInUser={setLoggedInUser} />
      <div>
        <p>Not on schmoozio yet?</p>
        <Link to="/register">
          <button>Register</button>
        </Link>
      </div>
    </div>
  );
};

export default LoginPage;
