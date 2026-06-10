from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from config import settings
import models
from routes import auth_routes, expense_routes

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Ensure tables exist before serving requests.
    Base.metadata.create_all(bind=engine)

# Allow frontend dev server to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(expense_routes.router)


@app.get("/health")
def health_check():
    return {"status": "Expense Tracker API is alive!"}