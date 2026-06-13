from fastapi import FastAPI
from routers import orders, inventory  # <-- Added inventory here

app = FastAPI(title="Eluno AI Order Management Engine")

# Hook the routers into the main application
app.include_router(orders.router)
app.include_router(inventory.router)   # <-- Added this line

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "backend_api",
        "database_connected": True
    }