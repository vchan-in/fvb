import time, os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read the environment .env file in the root directory
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if os.path.exists(os.path.join(BASEDIR, ".env")):
    print(f"Loading environment variables from {os.path.join(BASEDIR, '.env')}")
    load_dotenv(os.path.join(BASEDIR, ".env"))

VBANK_DATABASE_HOST = os.getenv("VBANK_DATABASE_HOST", "db")
VBANK_DATABASE_NAME = os.getenv("VBANK_DATABASE_NAME", "vbank")
VBANK_DATABASE_USER = os.getenv("VBANK_DATABASE_USER", "root")
VBANK_DATABASE_PASSWORD = os.getenv("VBANK_DATABASE_PASSWORD", "vbank")

# Wait and retry to connect to the database
while True:
    try:
        engine = create_engine(f"mysql+mysqlconnector://{VBANK_DATABASE_USER}:{VBANK_DATABASE_PASSWORD}@{VBANK_DATABASE_HOST}:3306/{VBANK_DATABASE_NAME}")
        engine.connect()
        print(f"Connected to database {VBANK_DATABASE_NAME} at {VBANK_DATABASE_HOST} as {VBANK_DATABASE_USER} with password {VBANK_DATABASE_PASSWORD}")
        break
    except Exception as e:
        print(f"Connecting to database {VBANK_DATABASE_NAME} at {VBANK_DATABASE_HOST} as {VBANK_DATABASE_USER} with password {VBANK_DATABASE_PASSWORD}")
        print("Database not ready yet, retrying in 5 seconds")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create a new session
Session = SessionLocal()
