from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="SHL Assessment Recommender"
)

app.include_router(router)