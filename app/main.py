from fastapi import FastAPI, status,Request
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.responses import JSONResponse, HTMLResponse
from automatisation.auto_get_reservations import fetch_reservations
from dotenv import load_dotenv
from utils import test_encryption_key
import os
import uvicorn
from fastapi.staticfiles import StaticFiles
load_dotenv()

from routers import review_routes
from routers import room_routes
from routers import timeedit_routes
from routers import account
from routers import room_routes_v2
from routers import room_routes_v3
origins = []

scheduler = BackgroundScheduler()
app = FastAPI()
test_encryption_key()

app.include_router(room_routes.router)
app.include_router(room_routes_v2.router)
app.include_router(room_routes_v3.router)
app.include_router(review_routes.public_router)
app.include_router(review_routes.private_router)
app.include_router(timeedit_routes.router)
app.include_router(account.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def index():
    file_path = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(file_path, "templates", "index.html")
    html_content = open(html_path, "r", encoding="utf-8").read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
@app.get("/demo", response_class=HTMLResponse)
def demo():
    file_path = os.path.dirname(os.path.realpath(__file__))
    html_path = os.path.join(file_path, "templates", "demo.html")
    html_content = open(html_path, "r", encoding="utf-8").read()
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
@app.get("/ping", status_code=status.HTTP_200_OK, tags=["API Check"], summary="Check if the API is up")
def check():
    return {"message": "pong"}

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

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