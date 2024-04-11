from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from automatisation.auto_get_reservations import fetch_reservations
from dotenv import load_dotenv
import uvicorn

load_dotenv()

from routers import test

origins = []

scheduler = BackgroundScheduler()

# This is the context manager that will start and stop the scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(fetch_reservations, "interval", seconds=5)
    scheduler.start()
    print("Scheduler started")
    try:
        yield
    finally:
        scheduler.shutdown()
        print("Scheduler stopped")


app = FastAPI( lifespan=lifespan)

app.include_router(test.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK, tags=["API Check"])
def check():
    return {
        "message": "Hello World!"
    }


if __name__ == '__main__':
    uvicorn.run(app)
