import random
from datetime import datetime
from faker import Faker

from data import models
from db.database import engine
from sqlalchemy.orm import Session
from handlers.main import get_password_hash_handler

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
            system_user = models.User(id=1, admin=0, username="system", password="AnikanSkywalkerIsTheChosenOne", hashed_password="AnikanSkywalkerIsTheChosenOne", email="system@vbank.vbank", phone="1234567890", address="local")
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
    
def seed_fake_users():
    # Dont create fake users if there are already 10 users
    with Session(engine) as session:
        user_count = session.query(models.User).count()
        if user_count >= 10:
            print("INFO:     Fake users already exists")
            return
        
    # Generate 43 fake users and thier accounts and transactions
    print("INFO:     Creating fake users. This may take a while")
    for _ in range(43):
        try:
            with Session(engine) as session:
                admin = 0
                username = fake.user_name()
                password = fake.password(length=8, special_chars=True, digits=True, upper_case=True, lower_case=True)
                hashed_password = get_password_hash_handler(password)
                email = fake.email()
                phone = fake.phone_number()
                address = fake.address()

                user = models.User(admin=admin, username=username, password=password, hashed_password=hashed_password, email=email, phone=phone, address=address)
                session.add(user)
                session.commit()
        except Exception as e:
            print(f"ERROR:    {e}")
            return
    print("INFO:     Users created")


def seed_fake_accounts():
    # Dont create fake accounts if there are already 50 accounts
    with Session(engine) as session:
        account_count = session.query(models.Account).count()
        if account_count >= 50:
            print("INFO:     Fake accounts already exists")
            return
        
    # Create between 1 and 5 accounts for each user and add between 100 and 1000 balance to each account
    print("INFO:     Creating fake accounts. This may take a while")
    try:
        with Session(engine) as session:
            users = session.query(models.User).all()
            for user in users:
                for _ in range(fake.random_int(1, 5)):
                    ''' 
                    Generate account number
                    Account number logic:
                    1. Prefix: VBANK
                    2. Random 4 digit number
                    3. Suffix: Timestamp format: YYYYDDHHMMSS
                    '''
                    try:
                        account_id = f"VBANK{str(random.randint(1000, 9999))}{datetime.now().strftime('%Y%d%H%M%S')}"
                        balance = fake.random_int(100, 1000)
                        account = models.Account(id=account_id, balance=balance, user_id=user.id)
                        session.add(account)
                        session.commit()
                    except:
                        session.rollback()
                        continue
    except Exception as e:
        print(f"ERROR:    {e}")
        return
    print("INFO:     Accounts created")


def seed_fake_transactions():
    # Dont create fake transactions if there are already 100 transactions
    with Session(engine) as session:
        transaction_count = session.query(models.Transaction).count()
        if transaction_count >= 100:
            print("INFO:     Fake transactions already exists")
            return
        
    # Create between 5 to 10 transactions for each account with other accounts of different users
    # Check balance before creating transaction to avoid negative balance
    print("INFO:     Creating fake transactions. This may take a while")
    for _ in range(10):
        try:
            with Session(engine) as session:
                accounts = session.query(models.Account).all()
                for account in accounts:
                    for _ in range(fake.random_int(5, 10)):
                        if account.balance > 0:
                            try:
                                amount = fake.random_int(1, account.balance)
                                description = fake.sentence(nb_words=5)
                                from_account_id = account.id
                                to_account_id = random.choice([acc.id for acc in accounts if acc.id != account.id])
                                transaction = models.Transaction(amount=amount, description=description, from_account_id=from_account_id, to_account_id=to_account_id)
                                session.add(transaction)
                                session.commit()
                                account.balance -= amount
                                session.commit()
                            except:
                                session.rollback()
                                continue
                        
        except Exception as e:
            print(f"ERROR:    {e}")
            return
    print("INFO:     Transactions created")


def seed():
    generate_tables()
    seed_default_users()
    seed_fake_users()
    seed_fake_accounts()
    seed_fake_transactions()
    print("INFO:     Seed completed")

if __name__ == "__main__":
    seed()
    
