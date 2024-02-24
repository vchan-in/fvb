import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Wait and retry to connect to the database
while True:
    try:
        engine = create_engine("mysql+mysqlconnector://root:password@db:3306/bank")
        engine.connect()
        break
    except Exception as e:
        print("Database not ready yet, retrying in 5 seconds")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create a new session
Session = SessionLocal()
