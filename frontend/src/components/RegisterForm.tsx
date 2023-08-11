import "./Forms.css";
import { useNavigate } from "react-router-dom";
import React, { useState, FormEvent } from "react";

const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;

const RegisterForm: React.FC = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const [emailError, setEmailError] = useState<string | null>(null);

  const validateEmail = (email: string) => {
    if (!emailRegex.test(email)) {
      setEmailError("Please provide a valid email address.");
      return false;
    }
    setEmailError(null);
    return true;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    const response = await fetch("http://localhost:8000/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, email, password }),
    });

    if (response.status === 200) {
      alert("Registered successfully");
      navigate("/login");
    } else {
      const data = await response.json();
      if (data.detail && typeof data.detail === "string") {
        setErrorMessage(data.detail);
      } else {
        setErrorMessage("Error registering user");
      }
    }
  };

  return (
    <div className="form-container">
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <form onSubmit={handleSubmit}>
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        {emailError && <div className="error-message">{emailError}</div>}
        <input
          type="email"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            validateEmail(e.target.value);
          }}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterForm;
