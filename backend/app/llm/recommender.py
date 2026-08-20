import os
import logging
from openai import OpenAI 
from dotenv import load_dotenv

# Load the environment variables from your .env file
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize the client pointing to Groq's FREE servers
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_resume_recommendations(job_description: str, resume_text: str, missing_skills: list) -> str:
    """
    Sends the job description, resume text, and identified missing skills 
    to the LLM to generate actionable, tailored resume improvement advice.
    Includes a fallback model in case the primary model fails.
    """
    prompt = f"""
    You are an expert career coach. 
    
    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}

    Missing Skills:
    {', '.join(missing_skills) if missing_skills else 'None identified'}

    Please provide feedback in exactly two sections using Markdown headers:

    ### 1. Skills to Learn
    List the specific skills missing from the resume that the job requires. 

    ### 2. How to Rewrite Your Resume
    Give 3 to 4 actionable bullet points on how to improve the resume for this specific job.
    """

    system_message = "You are a helpful career coach. Always provide a complete, well-formatted response."

    try:
        # ATTEMPT 1: Try the primary model specified in your .env file
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5, 
            max_tokens=1024 
        )
        return response.choices[0].message.content.strip()

    except Exception as primary_error:
        logger.warning(f"Primary model failed: {primary_error}. Switching to backup model...")
        
        try:
            # ATTEMPT 2: Fallback to a highly stable, older model if the primary fails
            backup_response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5, 
                max_tokens=1024 
            )
            return backup_response.choices[0].message.content.strip()
            
        except Exception as backup_error:
            logger.error(f"Both primary and backup models failed: {backup_error}")
            return "Our AI is currently undergoing maintenance. Please try again in a few minutes!"


def generate_cover_letter(job_description: str, resume_text: str) -> str:
    """
    Uses the LLM to write a tailored cover letter.
    Includes a fallback model in case the primary model fails.
    """
    prompt = f"""
    You are an expert career coach. Write a professional, highly tailored cover letter 
    for the candidate applying to the job described below.
    
    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}

    Instructions:
    - Keep it to 3-4 concise paragraphs.
    - Highlight the specific overlaps between the candidate's skills and the job requirements.
    - Adopt a confident, professional, and engaging tone.
    - Do not include placeholders like [Your Name] unless absolutely necessary, just write the core letter body.
    """

    system_message = "You are a professional cover letter writer."

    try:
        # ATTEMPT 1: Try the primary model
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL"),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, 
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()

    except Exception as primary_error:
        logger.warning(f"Primary model failed for cover letter: {primary_error}. Switching to backup...")
        
        try:
            # ATTEMPT 2: Fallback model
            backup_response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, 
                max_tokens=1024
            )
            return backup_response.choices[0].message.content.strip()

        except Exception as backup_error:
            logger.error(f"Both models failed for cover letter: {backup_error}")
            return "Could not generate cover letter at this time due to high server traffic. Please try again later."
            