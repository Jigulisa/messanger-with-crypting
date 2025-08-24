import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Chats(Base):
    __tablename__ = "chats"
    chat_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Numeric, ForeignKey("users.public_key"))
    description = Column(String, nullable=True)

class Users(Base):
    __tablename__ = "users"
    public_key = Column(Numeric, primary_key=True)
    username = Column(String, nullable=False)
    personal_data = Column(String)
    


class Messages(Base):
    __tablename__ = "messages"
    sent_time = Column(DateTime, nullable=False)
    message = Column(String, nullable=False)
    author_id = Column(Numeric, ForeignKey("users.public_key"))
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"))
    is_spam = Column(Boolean)

class HasAccess(Base):
    __tablename__ = "access"
    public_key_user = Column(Numeric, ForeignKey("users.public_key"))
    chat_id = Column(BigInteger, ForeignKey("chats.chat_id"))
    chat_key = Column(Numeric, unique=True, nullable=False)
    role = Column(String)
    last_seen = Column(DateTime, nullable=False)

engine = create_engine("sqlite:///mydb.sqlite")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()