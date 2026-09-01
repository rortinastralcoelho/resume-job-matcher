import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv

load_dotenv()

# This is the secret key used to sign the JWTs. 
# IN PRODUCTION: This should be a long, random string in your .env file!
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_temporary_key_123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Tells passlib to use bcrypt for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the hashed version in the database."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Converts a plain text password into a secure bcrypt hash."""
    return pwd_context.hash(password[:72])

def create_access_token(data: dict) -> str:
    """Generates a JWT token valid for a specific amount of time."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Creates the token string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt