# Python FastAPI Backend 

## Description
This is a backend run by a FastApi server. It is used to serve the frontend with data from the database.

## Installation
1. Clone the repository
2. Install the requirements

```bash
pip install -r requirements.txt
```
3. Run the server
```bash
python -m uvicorn --app-dir="./app" --reload main:app  --reload
```
## Testing
1. Run Tests
```bash
pytest app\test_main.py
```