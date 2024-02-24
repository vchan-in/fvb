from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from cmd.api.main import router as customer_router
from cmd.api.admin import router as admin_router

from cmd.seed.main import generate_tables

from handlers.gql import graphql_app


# Generate bank database tables
generate_tables()



methods = ["GET", "POST", "DELETE"]

app = FastAPI(redirect_slashes=False, title="vBank API", description="A vulnerable bank API", version="24.02")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# REST routes
app.include_router(customer_router, prefix="/api/v1", tags=["customer"])   # Include the customer router
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])   # Include the admin router

# GraphQL routes
app.include_router(graphql_app, prefix="/graphql")
app.add_websocket_route("/graphql", graphql_app)
