from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_, text
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import random

from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from data.models import User as UserModel, Account as AccountModel, Transaction as TransactionModel
from data.serializers import User, UserCreate, Account, AccountCreate, TransactionCreate, TransactionResponse,Deposit, TokenData, UserInDB
from db.database import SessionLocal, Session as DBSession
from utils.main import convert_to_utc

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"     # SecurityVuln: Weak algorithm used for encoding the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

#
#
# Action Handlers
#
#

# Create access token
def create_access_token_handler(data: dict, expires_delta: timedelta | None = None):
    '''
    Create access token

    Example usage:

        create_access_token_handler(data={"sub": "your_username"}, expires_delta=timedelta(minutes=15))

    Output:

        b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ5b3VyX3VzZXJuYW1lIiwiZXhwIjoxNjIyNzIwMzI3fQ.7
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Register User Handler
async def register_user_handler(db: Session, request: UserCreate) -> User:
    '''
    Register user
    
    Example usage:

        register_user_handler(request=UserModel(username="your_username", email="your_email", password="your_password", dob="your_dob", phone="your_phone", address="your_address"))

    Output:

        UserModel(admin=1, username="your_username", email="your_email", password="your_password", dob="your_dob", phone="your_phone", address="your_address")
    '''
    try:
        # Check if the user already exists
        user = db.query(UserModel).filter(UserModel.username == request.username).first()
        if user:
            raise ValueError("User with same username or email already exists")
        
        if request.admin is None:
            request.admin = 0

        user = UserModel (
                admin=request.admin,
                username=request.username,
                email=request.email,
                password=request.password,
                hashed_password=get_password_hash_handler(request.password),
                dob = convert_to_utc(request.dob),
                phone=request.phone,
                address=request.address
            )
        db.add(user)
        db.commit()
        db.refresh(user)
        return User(
            id=user.id,
            admin=user.admin,
            username=user.username,
            password=user.password,
            email=user.email,
            dob=user.dob.isoformat() + "Z",
            phone=user.phone,
            address=user.address
        )
    except Exception as e:
        db.rollback()
        raise e
    
# Create account handler
async def create_account_handler(db: Session, user: User) -> Account:
    '''
    Create account

    Example usage:

        create_account_handler()

    Output:

        {
            "account_number": "your_account_number",
            "balance": 0.0,
            "user_id": 1
        }
    '''
    try:
        ''' 
        Generate account number
        Account number logic:
        1. Prefix: FVB
        2. Random 4 digit number
        3. Suffix: Timestamp format: YYYYDDHHMMSS
        '''
        account_id = f"FVB{str(random.randint(1000, 9999))}{datetime.now().strftime('%Y%H')}"

        if not user:
            raise ValueError("User not found")
        
        # If the account is the 1st account of the user, add 1000 to the account balance as a welcome bonus
        accounts = db.query(AccountModel).filter(AccountModel.user_id == user.id).all()
        if len(accounts) == 0:
            balance = 1000.0
        else:
            balance = 0.0

        account = AccountModel(
            id=account_id,
            balance=balance,
            user_id=user.id
        )
        db.add(account)     ## SecurityVuln: User can create accounts without limit due to missing limit check which was 5 accounts per user
        db.commit()
        db.refresh(account)
        return account
    except Exception as e:
        db.rollback()
        raise e

# Create transaction handler
async def create_transaction_handler(db: Session, request: TransactionCreate, user: User) -> TransactionResponse:
    '''
    Create transaction

    Example usage:

        create_transaction_handler(request=TransactionCreate(amount=1000.0, description="your_description", from_account_id=1, to_account_id=2))

    Output:

        {
            "amount": 1000.0,
            "description": "your_description",
            "timestamp": "2021-02-24T00:00:00Z",
            "from_account_id": 1,
            "to_account_id": 2
        }
    '''
    try:
        # Verify if the from account belongs to the current user
        from_is_valid = db.query(AccountModel).filter(or_(AccountModel.user_id == user.id, AccountModel.id == request.from_account_id)).first() ## Security Vuln: Changed from == to or_ to allow any user to transfer from any account
        if not from_is_valid:
            raise Exception("Invalid from account")
        
        from_account = db.query(AccountModel).filter(AccountModel.id == request.from_account_id).first() ## Security Vuln: Not checking if from_account_id is authorized to be used by the user
        to_account = db.query(AccountModel).filter(AccountModel.id == request.to_account_id).first()
        
        if not from_account or not to_account:
            raise Exception("Account not found")
        # if from_account.balance < request.amount:  ## Security Vuln: Commented out to allow negative balance
        #     raise Exception("Insufficient balance")

        from_account.balance -= request.amount
        to_account.balance += request.amount
        db.commit()

        transaction = TransactionModel(
            amount=request.amount,
            description=request.description,
            from_account_id=from_account.id,
            to_account_id=to_account.id
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return TransactionResponse(
            from_account=from_account,
            to_account=to_account,
            amount=transaction.amount,
            description=transaction.description,
            timestamp=transaction.timestamp.isoformat() + "Z"
        )
    except Exception as e:
        db.rollback()
        raise e
    
# Create deposit handler
async def create_deposit_handler(db: Session, request: Deposit, user: User) -> TransactionResponse:
    '''
    Create deposit

    Example usage:

        create_deposit_handler(request=Deposit(amount=1000.0, description="remote deposit", to_account_id=2))

    Output:

        {
            "amount": 1000.0,
            "description": "remote deposit",
            "timestamp": "2021-02-24T00:00:00Z",
            "from_account_id": 2,
            "to_account_id": 2
        }
    '''
    try:
        to_account = db.query(AccountModel).filter(AccountModel.id == request.to_account_id).first()
        
        to_account.balance += request.amount
        db.commit()
        
        transaction = TransactionModel(
            amount=request.amount,
            description=request.description,
            from_account_id=to_account.id,  # Deposit is from the account itself
            to_account_id=to_account.id
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return TransactionResponse(
            from_account=to_account,
            to_account=to_account,
            amount=transaction.amount,
            description=transaction.description,
            timestamp=transaction.timestamp.isoformat() + "Z"
        )
    except Exception as e:
        db.rollback()
        raise e
    
# Delete user handler for admin
async def admin_delete_user_handler(db: Session, user_id: int):
    '''
    Delete user

    Example usage:

        admin_delete_user_handler(user_id=1)

    Output:

        {
            "status": "success",
            "message": "User deleted successfully"
        }
    '''
    try:
        # Replace all the ForeignKey references to the user with Null
        accounts = db.query(AccountModel).filter(AccountModel.user_id == user_id).all()
        for account in accounts:
            account.user_id = 0
        db.commit()

        # Delete the user
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise e

#
#
# Read Handlers
#
#

async def authenticate_user_handler(db, username: str, password: str):
    user = await get_user_handler(db, username)
    if not user:
        return False
    if not verify_password_handler(password, user.hashed_password):
        return False
    return user


def verify_password_handler(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


def get_password_hash_handler(password):
    return pwd_context.hash(password)


async def get_user_handler(db, username: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.username == username).first()


async def get_user_me_handler(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Username not found")
        token_data = TokenData(username=username)
    except JWTError:
        raise Exception("JWT error")
    user = await get_user_handler(DBSession, username=token_data.username)
    if user is None:
        raise Exception("User not found")
    return user

async def get_current_user_handler(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_handler(DBSession, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_user_by_username_handler(db: Session, username: str):
    '''
    Get user by username
    '''
    try:
        records = text(f"SELECT * FROM users WHERE username LIKE '{username}'")  ## Security Vuln: SQL Injection
        db_results = db.execute(records)
        if db_results.rowcount > 1:     # Deliberately checking for > 1 to return multiple records
            records = []
            for result in db_results:
                result_dict = {
                    "id": result.id,
                    "email": result.email,
                    "hashed_password": result.hashed_password,
                    "phone": result.phone,
                    "admin": result.admin,
                    "username": result.username,
                    "password": result.password,
                    "dob": result.dob.isoformat() + "Z",
                    "address": result.address
                }
                records.append(result_dict)
        else:
            records = db_results.fetchone()
            records = {
                "id": records.id,
                "email": records.email,
                "hashed_password": records.hashed_password,
                "phone": records.phone,
                "admin": records.admin,
                "username": records.username,
                "password": records.password,
                "dob": records.dob.isoformat() + "Z",
                "address": records.address
            }
    except Exception as e:
        records = e
    return records

# Get all accounts of a user handler
async def get_all_accounts_of_user_handler(db: Session, user_id: int):
    '''
    Get all accounts of a user
    '''
    return db.query(AccountModel).filter(AccountModel.user_id == user_id).all()

# Get all transactions of a user handler
async def get_all_transactions_of_user_handler(db: Session, user_id: int):
    '''
    Get all transactions of a user
    '''
    # Get all accounts of the user
    accounts = db.query(AccountModel).filter(AccountModel.user_id == user_id).all()
    account_ids = [account.id for account in accounts]
    list_of_transactions = []
    for account_id in account_ids:
        transactions = db.query(TransactionModel).filter(TransactionModel.from_account_id == account_id).all()
        for transaction in transactions:
            transaction.timestamp = transaction.timestamp.isoformat() + "Z"
            list_of_transactions.append(transaction)
        # list_of_transactions.extend(transactions)
    return list_of_transactions


#
#
# Get All Queries Handlers for Admin
#
#

async def get_all_users_handler(db: Session):
    '''
    Get all users
    '''
    return db.query(UserModel).all()

async def get_all_accounts_handler(db: Session):
    '''
    Get all accounts
    '''
    return db.query(AccountModel).all()

async def get_all_transactions_handler(db: Session):
    '''
    Get all transactions
    '''
    return db.query(TransactionModel).all()