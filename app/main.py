"""Main FastAPI app module with health check and logging"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/", include_in_schema=False)
async def redirect_to_helloworld():
    """Redirect root to /helloworld with a hint message"""
    logger.info("Root (/) endpoint hit — suggesting /helloworld")
    return JSONResponse({"hint": "Try /helloworld"})

@app.get("/helloworld", response_class=JSONResponse)
async def read_root(request: Request):
    """Root endpoint returning JSON status"""
    logger.info(f"/helloworld hit from {request.client.host}")
    return {"status": "OK"}

@app.get("/healthz", response_class=JSONResponse)
async def health_check(request: Request):
    """Returns health check status"""
    logger.info(f"/healthz hit from {request.client.host}")
    return {"status": "healthy"}
    