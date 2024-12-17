from fastapi import FastAPI
from database import engine, Base
from routes import admin, customer, access_control, user

# Initialize Database Tables
print("Initializing database...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")


app = FastAPI()

# Include routes
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(customer.router, prefix="/customer", tags=["Customer"])
app.include_router(access_control.router, prefix="/access", tags=["Access Control"])
app.include_router(user.router, prefix="/user", tags=["User"])

@app.get("/")
def read_root():
    return {"message": "Cloud Service Access Management System"}
