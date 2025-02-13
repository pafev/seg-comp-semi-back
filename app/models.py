from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String, Text
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)
    files_received = relationship(
        "File", back_populates="receiver", foreign_keys="File.receiver_id"
    )


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_base64 = Column(Text)
    file_type = Column(String)
    receiver_id = Column(Integer, ForeignKey("users.id"))
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="files_received"
    )
    sender_id = Column(Integer, ForeignKey("users.id"))
    sender = relationship(
        "User",
        foreign_keys=[sender_id],
    )
    signature = Column(String)
    public_key = Column(String)
