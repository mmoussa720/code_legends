import uuid

from sqlalchemy import String,Boolean
from sqlalchemy.orm import mapped_column,Mapped,relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Text
from ...infrastructure.database.session import Base
from uuid import UUID
class Fighter(Base):
    __tablename__="fighter"
    first_name:Mapped[str]=mapped_column(String)
    last_name:Mapped[str]=mapped_column(String)
    email:Mapped[str]=mapped_column(String)
    user_name:Mapped[str]=mapped_column(String)
    hashed_password:Mapped[str]=mapped_column(Text)
    id: Mapped[str] = mapped_column("id", unique=True, primary_key=True, default=str(uuid.uuid4()))
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_image_url:Mapped[str]=mapped_column(String,default="https://profileimageurl.com")
    