import random
from datetime import datetime
from faker import Faker

from data import models
from db.database import engine
from sqlalchemy.orm import Session
from handlers.main import get_password_hash_handler
from sqlalchemy import text

fake = Faker()

def generate_tables():
    models.Base.metadata.create_all(bind=engine)
    print("INFO:     Tables created")

def seed_default_users():
    # Create system user with ID 1
    try:
        with Session(engine) as session:
            system_user = session.query(models.User).filter(models.User.id == 1).first()
            if system_user:
                print("INFO:     System user already exists")
                return
            system_user = models.User(id=1, admin=0, username="system", password="AnikanSkywalkerIsTheChosenOne", hashed_password="AnikanSkywalkerIsTheChosenOne", email="system@fvb.fvb", phone="1234567890", address="local")
            session.add(system_user)
            session.commit()
    except Exception as e:
        print(f"ERROR:    {e}")
        return

    # Create admin user with ID 2
    try:
        with Session(engine) as session:
            admin_user = session.query(models.User).filter(models.User.id == 2).first()
            if admin_user:
                print("INFO:     Admin user already exists")
                return
            admin_user = models.User(id=2, admin=1, username="admin", password="password", hashed_password=get_password_hash_handler("password"), email="admin@example.com", phone="1234567890", address="local")
            session.add(admin_user)
            session.commit()
    except Exception as e:
        print(f"ERROR:    {e}")
        return
    
    print("INFO:     Default users created")


# Create a seed.sql file with the fake data on 143 users, each user with 1 to 5 accounts and each account with 5 to 10 transactions with other accounts. No data should be duplicate, so maintain a list to avoid duplicates
def seed_fake_data_sql():
    users = []
    accounts = []
    transactions = []

    # Generate 1143 fake users
    # Start with user ID 3
    user_id = 2
    for _ in range(1143):
        id = user_id + 1
        admin = 0
        username = fake.user_name()
        password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
        hashed_password = get_password_hash_handler(password)
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d %H:%M:%S')
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()
        # Check if user already exists
        if username not in [user['username'] for user in users]:
            users.append({"id": id, "admin": admin, "username": username, "password": password, "hashed_password": hashed_password, "dob": dob, "email": email, "phone": phone, "address": address})
            user_id += 1
            print(f"INFO:     {username} created")
        else:
            continue
    print ("INFO:     Fake users generated")

    # Generate between 1 and 5 accounts for each user
    account_count = 0
    for user in users:
        # Get user id from the user string
        for _ in range(fake.random_int(1, 5)):
            account_id = f"FVB{str(random.randint(1000, 9999))}{datetime.now().strftime('%Y%H')}"
            balance = fake.random_int(100, 1000)
            # Check if account already exists
            if account_id not in [acc['id'] for acc in accounts]:
                accounts.append({"id": account_id, "balance": balance, "user_id": user["id"]})
                account_count += 1
                print(f"INFO:     Account {account_id} created")
            else:
                continue
    print("INFO:     Fake accounts generated")

    # Create between 5 to 10 transactions for each account with other accounts of different users
    for account in accounts:
        for _ in range(fake.random_int(5, 10)):
            amount = fake.random_int(1, account["balance"])
            description = fake.sentence(nb_words=2)[:15]
            from_account_id = account["id"]
            to_account_id = random.choice([acc["id"] for acc in accounts if acc["id"] != account["id"]])
            timestamp = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            transactions.append({"amount": amount, "description": description, "from_account_id": from_account_id, "to_account_id": to_account_id, "timestamp": timestamp})
    print("INFO:     Fake transactions generated")
    
    # Write the fake data to a seed.txt file
    with open("seed.txt", "w") as f:
        # First, write all users to the file
        for user in users:
            f.write(f"INSERT INTO users (id, admin, username, password, hashed_password, dob, email, phone, address) VALUES ({user['id']}, {user['admin']}, '{user['username']}', '{user['password']}', '{user['hashed_password']}', '{user['dob']}', '{user['email']}', '{user['phone']}', '{user['address']}');\n")
        
        # Then, write all accounts to the file
        for account in accounts:
            f.write(f"INSERT INTO accounts (id, balance, user_id) VALUES ('{account['id']}', {account['balance']}, {account['user_id']});\n")
        
        # Finally, write all transactions to the file
        for transaction in transactions:
            f.write(f"INSERT INTO transactions (amount, description, from_account_id, to_account_id, timestamp) VALUES ({transaction['amount']}, '{transaction['description']}', '{transaction['from_account_id']}', '{transaction['to_account_id']}', '{transaction['timestamp']}');\n")
    
    print("INFO:     Fake data written to seed.txt file")


def insert_fake_data_txt():
    try:
        with open("seed.txt", "r") as f:
            statements = f.read().split(';')
            with Session(engine) as session:
                for statement in statements:
                    try:
                        session.execute(text(statement))
                        session.commit()
                    except Exception as e:
                        print(f"ERROR:    {e}")
                        session.rollback()
    except Exception as e:
        print(f"ERROR:    {e}")

    print("INFO:     Fake data inserted into database")

# Import the fvb.sql file into the database
def seed_fvb_sql():
    try:
        with open("fvb.sql", "r") as f:
            statements = f.read().split(';')
            with Session(engine) as session:
                for statement in statements:
                    try:
                        session.execute(text(statement))
                        session.commit()
                    except Exception as e:
                        print(f"ERROR:    {e}")
                        session.rollback()
    except Exception as e:
        print(f"ERROR:    {e}")

    print("INFO:     fvb.sql file imported into database")
    

def seed():
    generate_tables()
    seed_default_users()
    # seed_fake_data_sql()
    insert_fake_data_txt()
    # seed_fvb_sql()
    

if __name__ == "__main__":
    seed()
    
