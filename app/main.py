from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import create_db_and_tables
from app.exceptions import AuthError
import logging

# Correctly import the router objects from the route modules
from app.routes.specs import router as specs_router 
from app.routes.sdk import router as sdk_router # Assuming sdk.py also has a 'router' variable
from app.routes.projects import router as projects_router # Import projects router

# Import routes here (will be done in later commits)
# from app.routes import sdk_router

description = """
Devity Core Backend API
"""


tags_metadata = [

]

# Define the startup event handler
async def startup_event():
    print("Application startup...")
    # Call the function to create tables on startup
    create_db_and_tables()
    print("Application startup complete.")

# notice that the app instance is called `app`, this is very important.
app = FastAPI(
    title="Devity Backend Server",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata,
    on_startup=[startup_event] # Register the startup event
)

# CORS Configuration
# TODO: Restrict origins for production
origins = [
    "http://localhost",
    "http://localhost:8080", # Default flutter run web port
    "http://localhost:8000", # Sometimes used for web dev
    # Add other origins if needed (e.g., your deployed console URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
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

# Include the specs router
app.include_router(specs_router, prefix="/specs", tags=["Specs"])
# Include the sdk router
app.include_router(sdk_router, prefix="/sdk", tags=["SDK"])
# Include the projects router
app.include_router(projects_router, prefix="/projects", tags=["Projects"])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/ping")
async def ping():
    return {"message": "pong"}
