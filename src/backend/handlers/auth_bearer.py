from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"     # SecurityVuln: Weak algorithm used for encoding the JWT token
ACCESS_TOKEN_EXPIRE_MINUTES = 1

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.validate_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token")
            # if not self.validate_jwt_expired(credentials.credentials):        # SecurityVuln: No token expiration check
            #     raise HTTPException(status_code=403, detail="Token expired")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
    
    @staticmethod
    def decode_jwt(token):
        try:
            # Decode and verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
            return payload
        except JWTError:
            # Handle the error if the token is invalid
            return None
        
    @staticmethod
    def validate_jwt(token):
        try:
            # Decode and verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
            if payload:
                return True
        except JWTError:
            # Handle the error if the token is invalid
            return None
        
    @staticmethod
    def validate_jwt_expired(token):
        try:
            # Decode and verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            # Handle the error if the token is invalid
            return None