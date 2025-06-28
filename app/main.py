"""Main FastAPI app module with health check and logging"""

import logging
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/", response_class=PlainTextResponse)
async def read_root():
    """Returns a plain text OK status"""
    logger.info("Root endpoint hit")
    return "Hello, World! Status: OK"

@app.get("/healthz", response_class=JSONResponse)
async def health_check():
    """Returns health check status"""
    logger.info("Health check requested")
    return {"status": "healthy"}
