from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()

class DatabaseSettings(BaseSettings):
    DATABASE_URL:str=os.getenv("DATABASE_URL")
    

class settings(DatabaseSettings):
    pass 

settings=settings()
