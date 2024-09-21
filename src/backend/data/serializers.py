from pydantic import BaseModel
from typing import List, Optional
import strawberry


class Token(BaseModel): # Created for JWT module
    access_token: str
    token_type: str


class TokenData(BaseModel): # Created for JWT module
    username: str | None = None


class User(BaseModel):
    id: int
    admin: int
    username: str
    email: str
    password: str
    dob: str
    phone: str
    address: str

    class Config:
        from_attributes = True

@strawberry.type
class UserGQL():
    id: int
    admin: int
    username: str
    email: str
    dob: str
    phone: str
    address: str

class UserInDB(User): # Created for JWT module
    hashed_password: str

class Account(BaseModel):
    id: str
    balance: float
    user_id: int

    class Config:
        from_attributes = True

@strawberry.type
class AccountGQL():
    id: str
    balance: float
    user_id: int

class Transaction(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    timestamp: str
    from_account_id: str
    to_account_id: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    admin: int
    username: str
    email: str
    password: str
    dob: str
    phone: str
    address: str

class AccountCreate(BaseModel):
    user_id: int

class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str]
    from_account_id: str
    to_account_id: str

class TransactionResponse(BaseModel):
    from_account: Account
    to_account: Account
    amount: float
    description: Optional[str]
    timestamp: str

    class Config:
        from_attributes = True

@strawberry.type
class TransactionResponseGQL():
    from_account: str
    to_account: str
    amount: float
    description: Optional[str]
    timestamp: str
    
class Deposit(BaseModel):
    amount: float
    description: Optional[str]
    to_account_id: str

class AccountResponse(BaseModel):
    account: Account
    transactions: List[TransactionResponse]

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user: User
    accounts: List[Account]

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str