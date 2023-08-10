import './App.css';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import { useAuth } from './contexts/AuthContext';
import { User } from './SharedTypes';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';
import React, { useState, useEffect } from 'react';
import RegisterPage from './pages/RegisterPage';


const RedirectHandler: React.FC<{ userData: User | null }> = ({ userData }) => {
    const navigate = useNavigate();

    useEffect(() => {
        if (userData) {
            navigate('/main');
        } else {
            navigate('/login');
        }
    }, [userData, navigate]);

    return null;
}

const App: React.FC = () => {
    const [loggedInUser, setLoggedInUser] = useState<string | null>(() => localStorage.getItem('loggedInUser'));
    const [userData, setUserData] = useState<User | null>(null);
    
    const { logout, token } = useAuth();

    useEffect(() => {
        localStorage.setItem('loggedInUser', loggedInUser || '');
    }, [loggedInUser]);

    useEffect(() => {
        if (token !== null) {
            const fetchUserData = async () => {
                try {
                    const response = await fetch('http://localhost:8000/users/me', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('token')}`
                        }
                    });
                    
                    if (response.ok) {
                        const user = await response.json();
                        setUserData(user);
                    } else {
                        console.error("Failed to fetch user data.");
                        logout();
                    }
                } catch (error) {
                    console.error("Error fetching user data:", error);
                }
            };
    
            fetchUserData();
        }
    }, [token, logout]);

    return (
        <Router>
          <div className="container">
            {userData ? (
              <>
                <button onClick={() => {
                    logout();
                    setUserData(null);
                    }}>Logout</button>
              </>
            ) : null}
              
            <Routes>
              {userData ? (
                <>
                  <Route path="/main" element={<MainPage user={userData} />} />
                </>
              ) : (
                <>
                  <Route path="/login" element={<LoginPage setLoggedInUser={setLoggedInUser} />} />
                  <Route path="/register" element={<RegisterPage />} />
                </>
              )}
              <Route path="*" element={<RedirectHandler userData={userData} />} />
            </Routes>
          </div>
        </Router>
      );
}

export default App;
