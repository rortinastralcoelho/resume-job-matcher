import React, { useState } from 'react';

function ResumeUpload({ onResumeSubmit }) {
  const [file, setFile] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) {
      onResumeSubmit(file);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
      <div style={{ 
        border: '2px dashed #334155', 
        padding: '30px', 
        textAlign: 'center', 
        borderRadius: '12px', 
        backgroundColor: '#030712',
        transition: 'border-color 0.2s'
      }}
      onMouseOver={(e) => e.currentTarget.style.borderColor = '#a855f7'}
      onMouseOut={(e) => e.currentTarget.style.borderColor = '#334155'}
      >
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={(e) => setFile(e.target.files[0])}
          required
          style={{ color: '#cbd5e1', width: '100%', cursor: 'pointer' }}
        />
      </div>
      <button
        type="submit"
        style={{ 
          padding: '14px', 
          borderRadius: '8px', 
          border: 'none', 
          backgroundColor: '#a855f7', 
          color: 'white', 
          fontWeight: '600', 
          fontSize: '16px', 
          cursor: 'pointer', 
          transition: 'background-color 0.2s' 
        }}
        onMouseOver={(e) => e.target.style.backgroundColor = '#9333ea'}
        onMouseOut={(e) => e.target.style.backgroundColor = '#a855f7'}
      >
        Upload Resume
      </button>
    </form>
  );
}

export default ResumeUpload;