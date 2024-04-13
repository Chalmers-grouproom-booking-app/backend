from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from automatisation.auto_get_reservations import fetch_reservations
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

from app.routers import routes

origins = []

scheduler = BackgroundScheduler()

# This is the context manager that will start and stop the scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("AUTO_FETCH_RESERVATIONS") == "True":
        scheduler.add_job(fetch_reservations, "interval", seconds=5)
        scheduler.start()
        print("Scheduler started")
        try:
            yield
        finally:
            scheduler.shutdown()
            print("Scheduler stopped")
    else:
        yield


app = FastAPI( lifespan=lifespan)

app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["API Check"])
def check():
    print("Welcome, to the server")
    return {
        "message": "Hello World!"
    }


if __name__ == '__main__':
    print("JEL")
    uvicorn.run(app)
    
