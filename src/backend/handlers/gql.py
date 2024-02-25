import strawberry
import asyncio
from graphql.validation import NoSchemaIntrospectionCustomRule
from strawberry.extensions import AddValidationRules
from typing import AsyncGenerator
from fastapi import Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from typing import Generator
from functools import cached_property
from strawberry.fastapi import BaseContext, GraphQLRouter
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from data.models import User as UserModel
from data.serializers import UserGQL, AccountGQL, TransactionCreate, TransactionResponseGQL
from handlers.main import register_user_handler, get_current_user_handler, get_all_users_handler, get_user_by_username_handler, create_account_handler, get_all_accounts_of_user_handler, create_transaction_handler, get_all_accounts_handler, get_all_transactions_handler
from db.database import SessionLocal, Session as DBSession



def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Context(BaseContext): # Created for Strawberry GraphQL Auth
    @cached_property
    async def user(self) -> UserGQL | None:
        try:
            if not self.request:
                return None
    
            authorization = self.request.headers.get("Authorization", None)
            if not authorization:
                return None
            token = authorization.replace("Bearer ", "")
            current_user = await get_current_user_handler(token)
            return UserGQL(id=current_user.id, admin=current_user.admin, username=current_user.username, email=current_user.email)
        except Exception as e:
            return e
    
    @cached_property
    async def token(self) -> str | None:
        try:
            if not self.request:
                return None
    
            authorization = self.request.headers.get("Authorization", None)
            if not authorization:
                return None
            token = authorization.replace("Bearer ", "")
            return token
        except Exception as e:
            return e
    
Info = _Info[Context, RootValueType]
 
 
@strawberry.type
class Query:
    # Return pong
    @strawberry.field
    def ping(self) -> str:
        return "pong!"

    
    # Return user by username
    @strawberry.field
    async def get_user_by_username(self, info: Info, username: str) -> UserGQL:
        '''
        Get user by username

        Example usage:

        query {
            get_user_by_username(username: "your_username") {
                username
                email
                admin
                dob
                phone
                address
            }
        }
        '''
        try:
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            user =  await get_user_by_username_handler(DBSession, username)
            return UserGQL(id=user.id, admin=user.admin, username=user.username, email=user.email, dob=user.dob, phone=user.phone, address=user.address)
        except Exception as e:
            return e
    
    # Return all users
    @strawberry.field
    async def get_all_users(self, info: Info) -> list[UserGQL]:
        '''
        Get all users

        Example usage:

        query {
            get_users {
                username
                email
                admin
                dob
                phone
                address
            }
        }
        '''
        try:
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            users = await get_all_users_handler(DBSession)
            # Convert users to UserGQL
            users_gql = []
            for user in users:
                users_gql.append(UserGQL(id=user.id, admin=user.admin, username=user.username, email=user.email, dob=user.dob, phone=user.phone, address=user.address))
            return users_gql
        except Exception as e:
            return e
        
    # Return all accounts
    @strawberry.field
    async def get_all_accounts(self, info: Info) -> list[AccountGQL]:
        '''
        Get all accounts

        Example usage:

        query {
            get_all_accounts {
                account_number
                balance
                user_id
            }
        }
        '''
        try:
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            accounts = await get_all_accounts_handler(DBSession)
            accounts_gql = []
            for account in accounts:
                if account.user_id == None:
                    account.user_id = 0
                accounts_gql.append(AccountGQL(id=account.id, balance=account.balance, user_id=account.user_id))
            return accounts_gql
        except Exception as e:
            return e
    
    # Return all transactions
    @strawberry.field
    async def get_all_transactions(self, info: Info) -> list[TransactionResponseGQL]:
        '''
        Get all transactions

        Example usage:

        query {
            get_all_transactions {
                from_account
                to_account
                amount
                description
            }
        }
        '''
        try:
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            transactions = await get_all_transactions_handler(DBSession)
            transactions_gql = []
            for transaction in transactions:
                transactions_gql.append(TransactionResponseGQL(from_account=transaction.from_account_id, to_account=transaction.to_account_id, amount=transaction.amount, description=transaction.description, timestamp=transaction.timestamp))
            return transactions_gql
        except Exception as e:
            return e
    
    #
    #
    # User queries
    #
    #
        
    # Return authenticated user
    @strawberry.field
    async def get_authenticated_user(self, info: Info) -> UserGQL:
        '''
        Get authenticated user

        Example usage:

        query {
            get_authenticated_user {
                username
                email
                admin
            }
        }
        
        '''
        try:
            # Check if user is authenticated and return user
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            return user_context
        except Exception as e:
            return e


    # Query all my accounts
    @strawberry.field
    async def get_my_accounts(self, info: Info) -> list[AccountGQL]:
        '''
        Get my accounts

        Example usage:

        query {
            get_my_accounts(user_id: 1) {
                account_number
                balance
                user_id
            }
        }
        '''
        try:
            # Check if user is authenticated and return user
            user_context = await info.context.user
            if not user_context:
                raise Exception("Not authenticated")
            user_id = user_context.id
            accounts = await get_all_accounts_of_user_handler(DBSession, user_id)
            return accounts
        except Exception as e:
            return e
    

    
@strawberry.type
class Mutation:
    # Register user
    @strawberry.mutation
    async def create_user(self, username: str, email: str, password: str, admin: int = 0) -> UserGQL:
        '''
        Register user

        Example usage:

        mutation {
            register(username: "your_username", email: "your_email", password: "your_password", admin: 0) {
                username
                email
                admin
            }
        }
        '''
        try:
            user_model = UserModel(username=username, email=email, password=password, admin=admin)
            user = await register_user_handler(DBSession, user_model)
            return UserGQL(id=user.id, admin=user.admin, username=user.username, email=user.email)
        except Exception as e:
            return e
    
    # Create account
    @strawberry.mutation
    async def create_account(self, user_id: int) -> AccountGQL:
        '''
        Create account

        Example usage:

        mutation {
            create_account(user_id: 1) {
                id
                balance
                user_id
            }
        }
        '''
        try:
            account = await create_account_handler(DBSession, user_id)
            return AccountGQL(id=account.id, balance=account.balance, user_id=account.user_id)
        except Exception as e:
            return e
    
    # Create transaction
    @strawberry.mutation
    async def create_transaction(self, info: Info, amount: float, description: str, to_account_id: str) -> TransactionResponseGQL:
        '''
        Create transaction

        Example usage:

        mutation {
            create_transaction(amount: 1000.0, description: "your_description", from_account_id: "1", to_account_id: "2")
        }
        '''
        try:
            # Check if user is authenticated and return user
            user_context = await info.context.user
            token_context = await info.context.token
            if not user_context:
                raise Exception("Not authenticated")
            request = TransactionCreate(amount=amount, description=description, to_account_id=to_account_id)
            transaction = await create_transaction_handler(DBSession, request, token_context)
            return TransactionResponseGQL(from_account=transaction.from_account.id, to_account=transaction.to_account.id, amount=transaction.amount, description=transaction.description)
        except Exception as e:
            return e
            
    

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> AsyncGenerator[int, None]:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

 
def get_context() -> Context:
    return Context()

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
    # # Uncomment the following lines to disable introspection
	# extensions=[
	# 	AddValidationRules([NoSchemaIntrospectionCustomRule]),
	# ]
)
 
graphql_app = GraphQLRouter(schema, debug=True, allow_queries_via_get=True, graphiql=True, context_getter=get_context)