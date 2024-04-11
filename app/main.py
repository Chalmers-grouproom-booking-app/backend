from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi_utilities import repeat_every
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
import asyncio

load_dotenv()

from routers import test

origins = []


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Starting application")
#     background_task = asyncio.create_task( periodic_background_task() )
#     try:
#         yield
#     finally:
#         background_task.cancel()
#         try:
#             await background_task
#         except asyncio.CancelledError:
#             print("Background task was cancelled")

# async def periodic_background_task( secounds: int = 10 ):
#     try:
#         while True:
#             # Replace the print statement with the actual task you want to perform
#             print("Background task is running")
#             await asyncio.sleep( secounds )
#     except asyncio.CancelledError:
#         print("Periodic task was cancelled")
#     except Exception as e:
#         print(f"An error occurred in the background task: {e}")
# app = FastAPI( lifespan=lifespan)
app = FastAPI()

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
