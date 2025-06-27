"""Main FastAPI app module"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def read_root():
    """Returns a plain text OK status"""
    return "Hello, World! Status: OK"
