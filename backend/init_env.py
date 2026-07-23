import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('C:/SIGAP/backend/.env')
if env_path.exists():
    load_dotenv(env_path)
else:
    raise FileNotFoundError(f".env file not found at {env_path}")

print("Environment variables loaded successfully")
print(f"JWT_SECRET_KEY: {os.environ.get('JWT_SECRET_KEY')}")
