from data import models
from db.database import engine

def generate_tables():
    models.Base.metadata.create_all(bind=engine)
    print("INFO:     Tables generated successfully")
    
