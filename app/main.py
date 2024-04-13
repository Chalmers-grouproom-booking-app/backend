from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from automatisation.auto_get_reservations import fetch_reservations
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()

from routers import routes

origins = []

scheduler = BackgroundScheduler()


app = FastAPI()

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
    return {
        "message": "Hello World!"
    }


if __name__ == '__main__':
    if os.getenv("AUTO_FETCH_RESERVATIONS") == "True":
        scheduler.add_job(fetch_reservations, "interval", seconds=60*10)
        scheduler.start()
        print("Scheduler started to fetch reservations every 10 minutes")
        uvicorn.run(app, host="0.0.0.0", port=15029)
        print("Scheduler stopped")
        scheduler.shutdown()
    else:
        uvicorn.run(app, host="0.0.0.0", port=15029)