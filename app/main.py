from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from app.exceptions import AuthError
import logging
from app.database.database import init_db


description = """
"""


tags_metadata = [

]

# Initialize the database
init_db()

# notice that the app instance is called `app`, this is very important.
app = FastAPI(
    title="Devity Backend Server",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
)


# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.exception_handler(AuthError)
async def auth_error_handler(request, exc: AuthError):
    logger.error(f"Auth error: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred while authenticating the user."}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred."}
    )

# Include routes

# app.include_router(custom_auth_router, prefix="/auth",
#                    tags=["Custom Authentication Service"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/ping")
async def ping():
    return {"message": "pong"}
