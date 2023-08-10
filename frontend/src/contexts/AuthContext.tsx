import React, { createContext, useContext, useState, useEffect } from 'react';

interface AuthContextType {
    token: string | null;
    userId: string | null;
    setToken: React.Dispatch<React.SetStateAction<string | null>>;
    setUserId: React.Dispatch<React.SetStateAction<string | null>>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

interface AuthProviderProps {
    children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
    const [userId, setUserId] = useState<string | null>(() => localStorage.getItem('userId'));

    useEffect(() => {
        localStorage.setItem('token', token || '');
        if (userId) {
            localStorage.setItem('userId', userId);
        } else {
            localStorage.removeItem('userId');
        }
    }, [token, userId]);

    const logout = () => {
        setToken(null);
        setUserId(null); 
        localStorage.removeItem('token');
        localStorage.removeItem('userId');
        localStorage.removeItem('loggedInUser');
    };

    return (
        <AuthContext.Provider value={{ token, setToken, logout, setUserId, userId }}>
            {children}
        </AuthContext.Provider>
    );
};
