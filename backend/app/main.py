from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- NEW: Import your database tools ---
from app.core.database import engine, Base
from app.models.user import User  # This forces SQLAlchemy to "see" your new table

# Import your routers
from app.api import routes_job, routes_resume, routes_analysis, routes_auth

# --- NEW: Build the database tables if they don't exist ---
Base.metadata.create_all(bind=engine)
# --------------------------------------------------------

app = FastAPI(
    title="Resume-Job Matcher API",
    description="API for the AI-powered resume and job description matching engine.",
    version="1.0.0"
)

# --- THE MAGIC CORS BLOCK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------

# Wire up the routers we just built
app.include_router(routes_auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(routes_job.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(routes_resume.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(routes_analysis.router, prefix="/api/analysis", tags=["Analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Resume-Job Matcher API! The engine is running."}