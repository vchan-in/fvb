from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from data import models
from data import serializers
from handlers.main import register_user_handler, get_current_user_handler, get_all_users_handler

from db.database import SessionLocal
def get_db():
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

# Delete user route
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return JSONResponse(status_code=200, content={"status": "success", "message": "User deleted successfully"})
    return JSONResponse(status_code=404, content={"status": "error", "message": "User not found"})

# Delete all users route
@router.delete("/users")
def delete_all_users(db: Session = Depends(get_db)):
        db.query(models.Account).delete()
        db.commit()

        db.query(models.User).delete()
        db.commit()
        return JSONResponse(status_code=200, content={"status": "success", "message": "All users deleted successfully"})


#
#
# Read Handlers
#
#

# Get user by username route
@router.get("/users/{username}")
def get_user(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return JSONResponse(status_code=200, content={"status": "success", "message": "User retrieved successfully", "data": jsonable_encoder(user)})
    return JSONResponse(status_code=404, content={"status": "error", "message": "User not found"})

# Get all users route
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = get_all_users_handler(db)
    return JSONResponse(status_code=200, content={"status": "success", "message": "Users retrieved successfully", "data": jsonable_encoder(users)})

