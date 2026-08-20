import React, { useState } from 'react';
import { loginUserAPI, registerUserAPI } from '../api/index';

const Auth = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [focusedInput, setFocusedInput] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let data;
      if (isLogin) {
        data = await loginUserAPI(email, password);
      } else {
        data = await registerUserAPI(email, password);
      }
      
      localStorage.setItem('token', data.access_token);
      onLoginSuccess();
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      backgroundColor: '#050810',
      padding: '20px', 
      fontFamily: 'sans-serif' 
    }}>
      
      {/* --- MAIN SPLIT CONTAINER --- */}
      <div style={{ 
        display: 'flex',
        flexWrap: 'wrap',
        width: '100%', 
        maxWidth: '1000px', 
        backgroundColor: '#0f172a',
        borderRadius: '24px', 
        border: '1px solid #1e293b',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.6)' 
      }}>
        
        {/* =========================================
            LEFT SIDE: VISUAL PANEL 
        ========================================= */}
        <div style={{ flex: '1 1 400px', padding: '15px', display: 'flex' }}>
          <div style={{
            width: '100%',
            backgroundColor: '#030712',
            borderRadius: '16px',
            padding: '40px',
            position: 'relative',
            overflow: 'hidden',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start'
          }}>
            <h1 style={{ color: '#fff', fontSize: '36px', fontWeight: '600', lineHeight: '1.2', margin: '0 0 15px 0', zIndex: 10 }}>
              Convert your resume into <br/>
              <span style={{ background: 'linear-gradient(90deg, #a855f7, #3b82f6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                more interviews.
              </span>
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '16px', zIndex: 10, margin: '0' }}>
              AI-powered matching to help you land your dream job faster.
            </p>

            {/* CSS-generated "Light Rays" */}
            <div style={{ position: 'absolute', bottom: '-10%', left: '10%', width: '60px', height: '60%', background: 'linear-gradient(to top, rgba(168, 85, 247, 0.8), transparent)', filter: 'blur(10px)', zIndex: 1 }}></div>
            <div style={{ position: 'absolute', bottom: '-5%', left: '30%', width: '80px', height: '80%', background: 'linear-gradient(to top, rgba(59, 130, 246, 0.7), transparent)', filter: 'blur(15px)', zIndex: 1 }}></div>
            <div style={{ position: 'absolute', bottom: '-20%', left: '55%', width: '40px', height: '50%', background: 'linear-gradient(to top, rgba(16, 185, 129, 0.6), transparent)', filter: 'blur(8px)', zIndex: 1 }}></div>
          </div>
        </div>

        {/* =========================================
            RIGHT SIDE: CLEAN FORM 
        ========================================= */}
        <div style={{ flex: '1 1 400px', padding: '60px 50px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>

          <h2 style={{ margin: '0 0 10px 0', color: '#fff', fontSize: '28px', fontWeight: '700' }}>
            {isLogin ? 'Welcome Back' : 'Get Started'}
          </h2>
          <p style={{ margin: '0 0 35px 0', color: '#94a3b8', fontSize: '14px', borderBottom: '1px solid #1e293b', paddingBottom: '25px' }}>
            {isLogin ? 'Enter your credentials to access your dashboard.' : 'Welcome to AI Matcher — Let\'s create your account.'}
          </p>

          {error && (
            <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.1)', color: '#f87171', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '14px', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <label style={{ fontSize: '13px', color: '#cbd5e1' }}>Your email</label>
              <input 
                type="email" 
                placeholder="hi@aimatcher.com" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
                onFocus={() => setFocusedInput('email')}
                onBlur={() => setFocusedInput(null)}
                required
                style={{ 
                  padding: '14px 16px', 
                  borderRadius: '8px', 
                  backgroundColor: 'transparent', 
                  color: 'white', 
                  fontSize: '15px', 
                  outline: 'none',
                  border: focusedInput === 'email' ? '1px solid #3b82f6' : '1px solid #334155',
                  boxShadow: focusedInput === 'email' ? '0 0 0 3px rgba(59, 130, 246, 0.2)' : 'none',
                  transition: 'all 0.2s ease'
                }}
              />
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <label style={{ fontSize: '13px', color: '#cbd5e1' }}>{isLogin ? 'Password' : 'Create new password'}</label>
              <input 
                type="password" 
                placeholder="••••••••••" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                onFocus={() => setFocusedInput('password')}
                onBlur={() => setFocusedInput(null)}
                required
                style={{ 
                  padding: '14px 16px', 
                  borderRadius: '8px', 
                  backgroundColor: 'transparent', 
                  color: 'white', 
                  fontSize: '15px', 
                  outline: 'none',
                  border: focusedInput === 'password' ? '1px solid #a855f7' : '1px solid #334155',
                  boxShadow: focusedInput === 'password' ? '0 0 0 3px rgba(168, 85, 247, 0.2)' : 'none',
                  transition: 'all 0.2s ease'
                }}
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              style={{ 
                padding: '14px', 
                borderRadius: '8px', 
                border: 'none', 
                backgroundColor: '#3b82f6', 
                color: 'white', 
                fontWeight: '600',
                fontSize: '16px',
                cursor: loading ? 'not-allowed' : 'pointer',
                marginTop: '10px',
                transition: 'background-color 0.2s'
              }}
              onMouseOver={(e) => e.target.style.backgroundColor = '#2563eb'}
              onMouseOut={(e) => e.target.style.backgroundColor = '#3b82f6'}
            >
              {loading ? 'Processing...' : (isLogin ? 'Log In' : 'Create new account')}
            </button>
          </form>

          <div style={{ textAlign: 'center', marginTop: '25px', fontSize: '14px', color: '#94a3b8' }}>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span 
              onClick={() => setIsLogin(!isLogin)} 
              style={{ color: '#fff', cursor: 'pointer', fontWeight: '600', textDecoration: 'underline' }}
            >
              {isLogin ? 'Sign Up' : 'Login'}
            </span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default Auth;