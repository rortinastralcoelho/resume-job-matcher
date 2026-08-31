const BASE_URL = 'https://resume-job-matcher-0zpz.onrender.com/api';

export const saveJobAPI = async (jobData) => {
  const response = await fetch(BASE_URL + '/jobs/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(jobData),
  });
  return response.json();
};

export const uploadResumeAPI = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(BASE_URL + '/resumes/', {
    method: 'POST',
    body: formData,
  });
  return response.json();
};

export const runAnalysisAPI = async (resumeId, jobId) => {
  const response = await fetch(BASE_URL + '/analysis/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_id: resumeId, job_id: jobId }),
  });
  return response.json();
};

// --- NEW AUTHENTICATION APIS ---

export const registerUserAPI = async (email, password) => {
  const response = await fetch(BASE_URL + '/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Registration failed');
  }
  return response.json(); // Returns the JWT token
};

export const loginUserAPI = async (email, password) => {
  // FastAPI's OAuth2 expects data as form-urlencoded, not JSON
  const formData = new URLSearchParams();
  formData.append('username', email); // FastAPI defaults to looking for 'username'
  formData.append('password', password);

  const response = await fetch(BASE_URL + '/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed');
  }
  return response.json(); // Returns the JWT token
};