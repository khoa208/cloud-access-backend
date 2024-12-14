from fastapi import FastAPI

from routes import admin, customer, access_control

app = FastAPI()

# Include routes
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(customer.router, prefix="/customer", tags=["Customer"])
app.include_router(access_control.router, prefix="/access", tags=["Access Control"])

@app.get("/")
def read_root():
    return {"message": "Cloud Service Access Management System"}
