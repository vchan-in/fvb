from fastapi import APIRouter, Depends, Header
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from fastapi import HTTPException, status
from datetime import timedelta
# from fastapi.security import OAuth2PasswordRequestForm
from typing import Generator, Annotated

from data.models import User as UserModel
from data.serializers import User, UserCreate, Token, AccountCreate, UserLogin, TransactionCreate, Deposit
from db.database import SessionLocal
from handlers.main import ACCESS_TOKEN_EXPIRE_MINUTES
from handlers.main import get_user_me_handler, register_user_handler, authenticate_user_handler, get_current_user_handler, create_access_token_handler, get_user_by_username_handler, create_account_handler, get_all_accounts_of_user_handler, create_transaction_handler, create_deposit_handler, decode_jwt, get_all_transactions_of_user_handler
from handlers.auth_bearer import JWTBearer


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

# Ping route
@router.get("/ping")
def ping():
    return {"ping": "pong!"}

#
#
# Action Handlers
#
#

# Register user route
@router.post("/user/create")
async def register(request: UserCreate, db: Session = Depends(get_db)):
    '''
    Register user
    
    Example usage:

        {
            "admin": 1,
            "username": "your_username",
            "email": "your_email",
            "password": "your_password",
            "dob": "your_dob",
            "phone": "your_phone",
            "address": "your_address"
        }

    Output:

        {
            "status": "success",
            "message": "User created
            "data": {
                "id": 1,
                "admin": 1,
                "username": "your_username",
                "email": "your_email",
                "password": "your_password",
                "dob": "your_dob",
                "phone": "your_phone",
                "address": "your_address"
            }
        }
    '''
    try:
        user_model = UserModel(username=request.username, email=request.email, password=request.password, admin=request.admin, dob=request.dob, phone=request.phone, address=request.address)
        user = await register_user_handler(db, user_model)
        return JSONResponse(status_code=201, content={"status": "success", "message": "User created successfully", "data": jsonable_encoder(user)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

# Create access token
@router.post("/auth/token")
async def login_for_access_token(request: UserLogin, db: Session = Depends(get_db)) -> Token:
    '''
    Create access token

    Example usage:

        {
            "username": "your_username",
            "password": "your_password"
        }

    Output:

        {
            "access_token": "eyJxxxxxxxx"
            "token_type": "bearer"
        }
    '''
    user = await authenticate_user_handler(db, request.username, request.password)
    if not user:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Incorrect username or password"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token_handler(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Verify access token
@router.post("/auth/token/verify")
async def verify_token(request: Token) -> JSONResponse:
    '''
    Verify access token

    Example usage:

        {
            "access_token": "eyJxxxxxxxx"
            "token_type": "bearer"
        }

    Output:

        {
            "status": "success",
            "message": "Token is valid"
        }
    '''
    try:
        is_token_valid = decode_jwt(request.access_token)
        if not is_token_valid:
            raise Exception("Token is invalid")
        return JSONResponse(status_code=200, content={"status": "success", "message": "Token is valid"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

# Create account route
@router.post("/account/create", dependencies=[Depends(JWTBearer())])
async def create_account(db: Session = Depends(get_db), authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Create account
    
    Output:

        {
            "status": "success",
            "message": "Account created successfully",
            "data": {
                "id": 1,
                "account_number": "your_account_number",
                "balance": 0.0,
                "user_id": 1
            }
        }
    '''
    try:
        token = authorization[0].split(" ")[1]
        current_user = await get_user_me_handler(token)
        account = await create_account_handler(db, current_user)
        return JSONResponse(status_code=201, content={"status": "success", "message": "Account created successfully", "data": jsonable_encoder(account)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    
# Create Transaction route
@router.post("/transaction/create", dependencies=[Depends(JWTBearer())])
async def create_transaction(request: TransactionCreate, db: Session = Depends(get_db), authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Create transaction
    
    Example usage:

        {
            "amount": 1000.0,
            "description": "your_description",
            "from_account_id": 1,
            "to_account_id": 2
        }

    Output:

        {
            "status": "success",
            "message": "Transaction created successfully",
            "data": {
                "id": 1,
                "amount": 1000.0,
                "description": "your_description",
                "timestamp": "2021-05-30T00:00:00",
                "from_account_id": 1,
                "to_account_id": 2
            }
        }
    '''
    try:
        # Get current user id from the Authorization header bearer token
        token = authorization[0].split(" ")[1]
        current_user = await get_user_me_handler(token)
        transaction = await create_transaction_handler(db, request, current_user)
        return JSONResponse(status_code=201, content={"status": "success", "message": "Transaction created successfully", "data": jsonable_encoder(transaction)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})

# Create Deposit route
@router.post("/deposit/create", dependencies=[Depends(JWTBearer())])
async def deposit(request: Deposit, db: Session = Depends(get_db), authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Create deposit
    
    Example usage:
    {
        "type": "check",
        "amount": 1000.0,
        "description": "remote deposit",
        "to_account_id": 1,
        "check_front": "base64_encoded_image",
        "check_back": "base64_encoded_image"
    }
    
    Output:
    {
        "status": "success",
        "message": "Deposit created successfully",
        "data": {
            "id": 1,
            "amount": 1000.0,
            "description": "Remote deposit",
            "timestamp": "2021-05-30T00:00:00",
            "to_account_id": 1
        }
    }
    '''
    try:
        # Get current user id from the Authorization header bearer token
        token = authorization[0].split(" ")[1]
        current_user = await get_user_me_handler(token)
        transaction = await create_deposit_handler(db, request, current_user)
        return JSONResponse(status_code=201, content={"status": "success", "message": "Deposit created successfully", "data": jsonable_encoder(transaction)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
#
#
# Read Handlers
#
#

@router.get("/users/me", response_model=User, dependencies=[Depends(JWTBearer())])
async def get_users_me(authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Get my user details

    Output:

        {
            "id": 1,
            "admin": 1,
            "username": "your_username",
            "email": "your_email",
            "dob": "your_dob",
            "phone": "your_phone",
            "address": "your_address"
        }
    '''
    try:
        token = authorization[0].split(" ")[1]
        current_user = await get_user_me_handler(token)
        if current_user:
            return JSONResponse(status_code=200, content={"status": "success", "message": "User retrieved successfully", "data": jsonable_encoder(current_user)})
    except Exception as e:
        return JSONResponse(status_code=400, content={"status": "error", "message": str(e)})
    return JSONResponse(status_code=404, content={"status": "error", "message": "User not found"})

# Get user by username route
@router.get("/users/{username}", dependencies=[Depends(JWTBearer())])
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = await get_user_by_username_handler(db, username)
    if user:
        return JSONResponse(status_code=200, content={"status": "success", "message": "User retrieved successfully", "data": jsonable_encoder(user)})
    return JSONResponse(status_code=404, content={"status": "error", "message": "User not found"})

# Get my accounts route
@router.get("/accounts/me", dependencies=[Depends(JWTBearer())])
async def get_my_accounts(db: Session = Depends(get_db), authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Get my accounts

    Output:

        {
            "status": "success",
            "message": "Accounts retrieved successfully",
            "data": [
                {
                    "account_number": "your_account_number",
                    "balance": 0.0,
                    "user_id": 1
                }
            ]
        }
    '''
    token = authorization[0].split(" ")[1]
    current_user = await get_user_me_handler(token)
    accounts = await get_all_accounts_of_user_handler(db, current_user.id)
    if accounts:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Accounts retrieved successfully", "data": jsonable_encoder(accounts)})
    return JSONResponse(status_code=404, content={"status": "error", "message": "Accounts not found"})

# Get accouts by username route
@router.get("/accounts/{username}", dependencies=[Depends(JWTBearer())])
async def get_accounts_by_username(username: str, db: Session = Depends(get_db)):
    user = await get_user_by_username_handler(db, username)
    if user:
        accounts = await get_all_accounts_of_user_handler(db, user.id)
        if accounts:
            return JSONResponse(status_code=200, content={"status": "success", "message": "Accounts retrieved successfully", "data": jsonable_encoder(accounts)})
    return JSONResponse(status_code=404, content={"status": "error", "message": "Accounts not found"})

# Get my transactions route
@router.get("/transactions/me", dependencies=[Depends(JWTBearer())])
async def get_my_transactions(db: Session = Depends(get_db), authorization: Annotated[list[str] | None, Header()] = None):
    '''
    Get my transactions

    Output:

        {
            "status": "success",
            "message": "Transactions retrieved successfully",
            "data": [
                {
                    "amount": 1000.0,
                    "description": "your_description",
                    "timestamp": "2021-05-30T00:00:00",
                    "from_account_id": 1,
                    "to_account_id": 2
                }
            ]
        }
    '''
    token = authorization[0].split(" ")[1]
    current_user = await get_user_me_handler(token)
    transactions = await get_all_transactions_of_user_handler(db, current_user.id)
    if transactions:
        return JSONResponse(status_code=200, content={"status": "success", "message": "Transactions retrieved successfully", "data": jsonable_encoder(transactions)})
    
    return JSONResponse(status_code=404, content={"status": "error", "message": "Transactions not found"})
