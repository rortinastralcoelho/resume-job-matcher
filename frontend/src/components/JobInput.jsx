import React, { useState } from 'react';

function JobInput({ onJobSubmit }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [focusedInput, setFocusedInput] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    onJobSubmit({ title, description });
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
      <input
        type="text"
        placeholder="Job Title (e.g. Software Engineer)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        onFocus={() => setFocusedInput('title')}
        onBlur={() => setFocusedInput(null)}
        required
        style={{ 
          padding: '16px', 
          borderRadius: '12px', 
          border: focusedInput === 'title' ? '1px solid #3b82f6' : '1px solid #1e293b', 
          backgroundColor: '#030712', 
          color: '#fff', 
          fontSize: '15px',
          outline: 'none',
          boxShadow: focusedInput === 'title' ? '0 0 0 3px rgba(59, 130, 246, 0.2)' : 'none',
          transition: 'all 0.2s'
        }}
      />
      <textarea
        placeholder="Paste the full Job Description here..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        onFocus={() => setFocusedInput('desc')}
        onBlur={() => setFocusedInput(null)}
        required
        rows="6"
        style={{ 
          padding: '16px', 
          borderRadius: '12px', 
          border: focusedInput === 'desc' ? '1px solid #3b82f6' : '1px solid #1e293b', 
          backgroundColor: '#030712', 
          color: '#fff', 
          fontSize: '15px', 
          resize: 'vertical',
          outline: 'none',
          boxShadow: focusedInput === 'desc' ? '0 0 0 3px rgba(59, 130, 246, 0.2)' : 'none',
          transition: 'all 0.2s'
        }}
      />
      <button
        type="submit"
        style={{ 
          padding: '14px', 
          borderRadius: '8px', 
          border: 'none', 
          backgroundColor: '#3b82f6', 
          color: 'white', 
          fontWeight: '600', 
          fontSize: '16px', 
          cursor: 'pointer', 
          transition: 'background-color 0.2s' 
        }}
        onMouseOver={(e) => e.target.style.backgroundColor = '#2563eb'}
        onMouseOut={(e) => e.target.style.backgroundColor = '#3b82f6'}
      >
        Save Job Data
      </button>
    </form>
  );
}

export default JobInput;