from fastapi import FastAPI
from .database import engine, Base
from . import models

from .routers import bins , readings, alerts
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Bin Alert Backend")

app.include_router(bins.router)
app.include_router(readings.router)
app.include_router(alerts.router)
@app.get("/")
def root():
    return {"message": "Bin Alert Backend. Use /docs"}

@app.get("/health")
def health():
    return {"status":"ok"} 