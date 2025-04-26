# Devity Backend

A FastAPI-based backend server for the Devity application.

## Project Structure

```
devity_backend/
├── app/                      # Main application directory
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration settings
│   ├── utility.py           # Utility functions
│   ├── exceptions.py        # Custom exceptions
│   ├── __init__.py          # Package initialization
│   ├── database/            # Database related code
│   ├── routes/              # API route definitions
│   ├── schemas/             # Pydantic models and schemas
│   └── services/            # Business logic and services
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── run.sh                   # Script to run the application
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── .gitattributes          # Git attributes
```

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for database)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd devity_backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

1. Start the application using the run script:
```bash
./run.sh
```

### Docker Deployment

1. Build and start the containers:
```bash
docker-compose up --build
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

The application requires the following environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Algorithm for JWT token generation
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]
