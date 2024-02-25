from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    admin = Column(Integer, default=0)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(50))
    hashed_password = Column(String(100))
    dob = Column(DateTime(timezone=True), default=datetime.utcnow)
    phone = Column(String(50), nullable=True)
    address = Column(String(100), nullable=True)

    accounts = relationship("Account", back_populates="user", cascade="all, delete")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(50), primary_key=True, unique=True, index=True)
    balance = Column(Float, default=0.0)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="accounts", cascade="all, delete")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String(20), nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    from_account_id = Column(String(50), ForeignKey("accounts.id"))
    to_account_id = Column(String(50), ForeignKey("accounts.id"))