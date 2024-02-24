import time, os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read the environment .env file in the root directory of the monorepo
BASEDIR = os.path.abspath(os.path.dirname(__name__))
MONODIR = os.path.abspath(os.path.join(BASEDIR, "../../"))
if os.path.exists(os.path.join(MONODIR, ".env.dev")):   # Check if the .env.dev file exists if not use the .env file
    load_dotenv(os.path.join(MONODIR, ".env.dev"))
else:
    load_dotenv(os.path.join(MONODIR, ".env"))

VBANK_DATABASE_HOST = os.getenv("VBANK_DATABASE_HOST", "db")
VBANK_DATABASE_NAME = os.getenv("VBANK_DATABASE_NAME", "vbank")
VBANK_DATABASE_USER = os.getenv("VBANK_DATABASE_USER", "root")
VBANK_DATABASE_PASSWORD = os.getenv("VBANK_DATABASE_PASSWORD", "vbank")

# Wait and retry to connect to the database
while True:
    try:
        engine = create_engine(f"mysql+mysqlconnector://{VBANK_DATABASE_USER}:{VBANK_DATABASE_PASSWORD}@{VBANK_DATABASE_HOST}:3306/{VBANK_DATABASE_NAME}")
        engine.connect()
        break
    except Exception as e:
        print("Database not ready yet, retrying in 5 seconds")
        time.sleep(5)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create a new session
Session = SessionLocal()
