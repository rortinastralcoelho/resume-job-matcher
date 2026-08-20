import React, { useState, useEffect } from 'react';
import Home from './pages/Home';
import Auth from './components/Auth';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check if the user already has a token when the app loads
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <div className="min-h-screen bg-[#0d1117]">
      {/* Top Navigation Bar */}
      {isAuthenticated && (
        <div style={{ padding: '15px 30px', display: 'flex', justifyContent: 'flex-end', backgroundColor: '#1e293b', borderBottom: '1px solid #333' }}>
          <button 
            onClick={handleLogout}
            style={{ padding: '8px 16px', backgroundColor: '#ef4444', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Log Out
          </button>
        </div>
      )}

      {/* Main App Routing */}
      {isAuthenticated ? (
        <Home />
      ) : (
        <Auth onLoginSuccess={() => setIsAuthenticated(true)} />
      )}
    </div>
  );
}

export default App;