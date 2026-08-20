import os

class Settings:
    PROJECT_NAME: str = "Resume Job Matcher"
    # This URL connects to the Postgres database running inside your Docker container
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/resume_matcher")

settings = Settings()