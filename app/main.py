from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_scrape
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_scrape.router)
