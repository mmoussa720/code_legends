from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
from .session import async_session
import os
load_dotenv()
engine=create_engine(os.getenv("DATABASE_URL"))
sessionLocal=sessionmaker(autoflush=False,bind=engine)
