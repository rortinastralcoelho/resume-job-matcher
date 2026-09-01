import React, { useState } from 'react';
import JobInput from '../components/JobInput';
import ResumeUpload from '../components/ResumeUpload';
import { saveJobAPI, uploadResumeAPI, runAnalysisAPI } from '../api/index';
import ReactMarkdown from 'react-markdown';

function Home() {
  const [jobId, setJobId] = useState(null);
  const [resumeId, setResumeId] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [coverLetter, setCoverLetter] = useState("");
  const [isLoadingLetter, setIsLoadingLetter] = useState(false);

  const handleJobSubmit = async (data) => {
    try {
      const response = await saveJobAPI(data);
      setJobId(response.id);
      alert(`Job Saved Successfully! (ID: ${response.id})`);
    } catch (error) {
      alert("Failed to save job. Make sure your backend server is running.");
    }
  };

  const handleResumeSubmit = async (file) => {
    try {
      const response = await uploadResumeAPI(file);
      setResumeId(response.id);
      alert(`Resume Uploaded Successfully! (ID: ${response.id})`);
    } catch (error) {
      alert("Failed to upload. Make sure your backend server is running.");
    }
  };

  const handleMatch = async () => {
    setLoading(true);
    try {
      const result = await runAnalysisAPI(resumeId, jobId);
      setMatchResult(result);
    } catch (error) {
      alert("Analysis failed. Please check your backend terminal for errors.");
    }
    setLoading(false);
  };

  const handleGenerateCoverLetter = async () => {
    setIsLoadingLetter(true);
    try {const response = await fetch(`https://resume-job-matcher-0zpz.onrender.com/api/analysis/cover-letter?job_id=${jobId}&resume_id=${resumeId}`, {
        method: 'POST'
      });
      const data = await response.json();
      setCoverLetter(data.cover_letter);
    } catch (error) {
      console.error("Failed to generate cover letter", error);
    }
    setIsLoadingLetter(false);
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#050810', padding: '60px 20px', fontFamily: 'sans-serif' }}>
      
      <div style={{ 
        maxWidth: '850px', 
        margin: '0 auto', 
        padding: '50px 40px', 
        backgroundColor: '#0f172a', 
        border: '1px solid #1e293b', // Clean, subtle border instead of the glowing cyan one
        borderRadius: '24px', 
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.6)' 
      }}>
        
        {/* --- PREMIUM HEADER --- */}
        <div style={{ textAlign: 'center', marginBottom: '50px' }}>
          <h1 style={{ 
            margin: '0 0 10px 0', 
            fontSize: '38px',
            fontWeight: '800',
            background: 'linear-gradient(90deg, #d8b4fe 0%, #ffffff 50%, #67e8f9 100%)', // Matches Login screen exactly
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '1px'
          }}>
            AI RESUME MATCHER
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '15px', margin: 0 }}>
            Upload your CV and Target Job to generate a match score and custom cover letter.
          </p>
        </div>

        {/* --- STEP 1: TARGET JOB (Subtle Styling) --- */}
        <div style={{ 
          padding: '30px', 
          marginBottom: '30px', 
          borderRadius: '16px', 
          backgroundColor: 'rgba(59, 130, 246, 0.03)', 
          border: '1px solid rgba(59, 130, 246, 0.2)' 
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <span style={{ backgroundColor: '#3b82f6', color: '#fff', padding: '4px 12px', borderRadius: '50px', fontSize: '12px', fontWeight: 'bold', letterSpacing: '1px' }}>STEP 1</span>
            <h3 style={{ color: '#fff', margin: 0, fontSize: '18px' }}>Target Job Profile</h3>
          </div>
          <JobInput onJobSubmit={handleJobSubmit} />
        </div>

        {/* --- STEP 2: UPLOAD RESUME (Subtle Styling) --- */}
        <div style={{ 
          padding: '30px', 
          marginBottom: '40px', 
          borderRadius: '16px', 
          backgroundColor: 'rgba(168, 85, 247, 0.03)', 
          border: '1px solid rgba(168, 85, 247, 0.2)' 
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '20px' }}>
            <span style={{ backgroundColor: '#a855f7', color: '#fff', padding: '4px 12px', borderRadius: '50px', fontSize: '12px', fontWeight: 'bold', letterSpacing: '1px' }}>STEP 2</span>
            <h3 style={{ color: '#fff', margin: 0, fontSize: '18px' }}>Applicant Resume</h3>
          </div>
          <ResumeUpload onResumeSubmit={handleResumeSubmit} />
        </div>
        
        {/* --- MATCH BUTTON --- */}
        <div style={{ textAlign: 'center' }}>
          <button 
            onClick={handleMatch}
            disabled={!jobId || !resumeId || loading}
            style={{ 
              padding: '16px 45px', 
              fontSize: '18px', 
              background: (jobId && resumeId) ? 'linear-gradient(135deg, #064e3b 0%, #022c22 100%)' : '#1e293b', 
              color: (jobId && resumeId) ? '#34d399' : '#64748b', 
              border: (jobId && resumeId) ? '2px solid #10b981' : '2px solid #334155', 
              borderRadius: '50px', 
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '2px',
              cursor: (jobId && resumeId && !loading) ? 'pointer' : 'not-allowed',
              boxShadow: (jobId && resumeId) ? '0 10px 25px rgba(16, 185, 129, 0.3)' : 'none',
              transition: 'all 0.3s ease'
            }}
          >
            {loading ? 'Analyzing Data...' : 'Execute AI Match ✓'}
          </button>
        </div>

        {/* --- MATCH RESULTS SECTION (Unchanged) --- */}
        {matchResult && (
          <div style={{ marginTop: '50px', padding: '30px', border: '2px solid #10b981', borderRadius: '16px', background: '#0f172a', color: '#fff', boxShadow: '0 0 30px rgba(16, 185, 129, 0.3)' }}>
            <h2 style={{ textAlign: 'center', color: '#34d399', margin: '0 0 20px 0', textShadow: '0 0 15px rgba(16, 185, 129, 0.4)' }}>
              MATCH COMPLETE
            </h2>
            
            <div style={{ textAlign: 'center', marginBottom: '30px', fontSize: '28px', fontWeight: '900' }}>
              SCORE: <span style={{ color: '#34d399' }}>{matchResult.overall_score}%</span>
            </div>
            
            <div style={{ marginTop: '20px', textAlign: 'left' }}>
              <strong style={{ fontSize: '18px', color: '#93c5fd' }}>Feedback & Improvements:</strong>
              <div style={{ marginTop: '15px', lineHeight: '1.6', backgroundColor: '#1e293b', padding: '25px', borderRadius: '12px', border: '1px solid #334155' }}>
                <ReactMarkdown>{matchResult.feedback}</ReactMarkdown>
              </div>
            </div>

            <div style={{ marginTop: '40px', paddingTop: '30px', borderTop: '1px solid #334155' }}>
              <button 
                onClick={handleGenerateCoverLetter}
                disabled={isLoadingLetter}
                style={{
                  width: '100%',
                  padding: '18px',
                  fontSize: '18px',
                  fontWeight: 'bold',
                  backgroundColor: '#7c3aed', 
                  color: 'white',
                  border: 'none',
                  borderRadius: '12px',
                  cursor: isLoadingLetter ? 'not-allowed' : 'pointer',
                  opacity: isLoadingLetter ? 0.7 : 1,
                  boxShadow: '0 0 20px rgba(124, 58, 237, 0.5)'
                }}
              >
                {isLoadingLetter ? "Writing Letter..." : "Generate AI Cover Letter ✉️"}
              </button>

              {coverLetter && (
                <div style={{ marginTop: '30px', padding: '30px', backgroundColor: '#1e293b', border: '2px solid #a855f7', borderRadius: '12px', textAlign: 'left', boxShadow: '0 0 20px rgba(168, 85, 247, 0.2)' }}>
                  <h3 style={{ margin: '0 0 20px 0', fontSize: '22px', color: '#d8b4fe' }}>Your Tailored Cover Letter</h3>
                  <p style={{ whiteSpace: 'pre-wrap', color: '#cbd5e1', lineHeight: '1.8', margin: 0 }}>
                    {coverLetter}
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Home;