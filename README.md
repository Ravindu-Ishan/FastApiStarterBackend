# FastAPI Starter Template

A production-ready FastAPI starter template with clean architecture, SQLAlchemy Core, and support for multiple databases including MySQL, Oracle, and SQLite.

## Architecture

```
src/
├── config/              # Configuration management
│   ├── app_config.py   # TOML and env variable reader
│   ├── database_config.py  # Database connection manager
│   └── log_config.py   # Logging configuration
├── model/              # SQLAlchemy Core table definitions
│   └── user.py        # User model
├── schema/             # Pydantic DTOs (Request/Response)
│   ├── user.py        # User schemas
│   └── common.py      # Common schemas
├── repository/         # Data access layer
│   └── user_repository.py
├── service/            # Business logic layer
│   └── user_service.py
├── controller/         # API endpoints (APIRouter)
│   └── user_controller.py
├── common/             # Shared utilities
│   └── util/          # Utility functions
│       ├── banner.py  # Startup banner
│       └── openapi_generator.py  # OpenAPI schema generator
├── deployment.toml     # Configuration file
└── main.py            # Application entrypoint
```

## Features

- **Clean Architecture**: Separated layers (Controller → Service → Repository → Model)
- **SQLAlchemy Core**: Direct SQL control with table definitions
- **Multi-Database Support**: MySQL, Oracle, and SQLite with easy switching
- **Configuration Management**: TOML-based config with environment variable overrides
- **Structured Logging**: Colorized console output with pipe-delimited format
- **Startup Banner**: Application information display on startup
- **FastAPI Best Practices**: APIRouter, dependency injection, Pydantic validation
- **RESTful API**: Complete CRUD operations with proper HTTP methods
- **Auto-generated Docs**: Swagger UI and ReDoc
- **CORS Support**: Configurable CORS middleware
- **OpenAPI Schema**: Auto-generated OpenAPI specification file
- **Scalable Structure**: Easy to extend with new features

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL, Oracle, or SQLite database

### Installation

1. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Configure application**:
   
   Create `.env` file from `.env.example`:
   ```bash
   # Database Configuration
   DB_TYPE=sqlite
   DB_HOST=localhost
   DB_PORT=3306
   DB_USERNAME=root
   DB_PASSWORD=your_password
   DB_DATABASE=fastapi_db
   
   # Application Configuration
   DEBUG=false
   LOG_LEVEL=INFO
   DETAILED_LOGS=false
   LOG_TO_FILE=true
   
   # Server Configuration
   SERVER_HOST=0.0.0.0
   SERVER_PORT=8000
   SERVER_RELOAD=true
   ```

   Or edit `deployment.toml` directly:
   ```toml
   [database]
   db_type = "${DB_TYPE}"
   host = "${DB_HOST}"
   port = ${DB_PORT}
   username = "${DB_USERNAME}"
   password = "${DB_PASSWORD}"
   database = "${DB_DATABASE}"
   
   [application]
   app_name = "FastAPI Starter"
   api_prefix = "/api/v1"
   debug = ${DEBUG}
   
   [logging]
   log_level = "${LOG_LEVEL}"
   detailed_logs = ${DETAILED_LOGS}
   log_to_file = ${LOG_TO_FILE}
   log_dir = "logs"
   
   [cors]
   origins = ["*"]
   
   [server]
   host = "${SERVER_HOST}"
   port = ${SERVER_PORT}
   reload = ${SERVER_RELOAD}
   ```

3. **Create database** (MySQL example):
   ```sql
   CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

### Running the Application

```powershell
python src/main.py
```

Or with uvicorn directly:
```powershell
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check and API information |

### Users API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users/` | Get all users (paginated) |
| POST | `/api/v1/users/` | Create new user |
| GET | `/api/v1/users/{user_id}` | Get user by ID |
| GET | `/api/v1/users/username/{username}` | Get user by username |
| PUT | `/api/v1/users/{user_id}` | Update user |
| DELETE | `/api/v1/users/{user_id}` | Delete user |

### Example Requests

**Health Check**:
```bash
curl "http://localhost:8000/"
```

**Create User**:
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

**Get Users (Paginated)**:
```bash
curl "http://localhost:8000/api/v1/users/?page=1&page_size=10"
```

## Database Support

### SQLite (Default)
```toml
[database]
db_type = "sqlite"
database = "fastapi.db"
```

### MySQL
```toml
[database]
db_type = "mysql"
host = "localhost"
port = 3306
username = "root"
password = "password"
database = "fastapi_db"
```

### Oracle
```toml
[database]
db_type = "oracle"
host = "localhost"
port = 1521
username = "system"
password = "password"
database = "XEPDB1"
service_name = "ORCL"
```

## Configuration

### Configuration Priority

1. **Environment Variables** (highest priority)
2. **deployment.toml** (default values)

Environment variables in `.env` file are automatically loaded and can override TOML values using `${VARIABLE_NAME}` syntax.

### Configuration Sections

**[database]** - Database connection settings
- `db_type`: Database type (sqlite, mysql, oracle)
- `host`, `port`, `username`, `password`, `database`: Connection details

**[application]** - Application settings
- `app_name`: Application name
- `api_prefix`: API route prefix
- `debug`: Enable FastAPI debug mode

**[logging]** - Logging configuration
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `detailed_logs`: Include file location in logs
- `log_to_file`: Enable file logging
- `log_dir`: Log file directory

**[cors]** - CORS configuration
- `origins`: Allowed origins (use ["*"] for all)

**[server]** - Server settings
- `host`: Server host address
- `port`: Server port
- `reload`: Enable auto-reload on code changes

## Logging

The application uses a structured logging format:

```
LEVEL | TIMESTAMP | LOGGER_NAME | MESSAGE
```

- Console output is colorized (INFO=green, WARNING=yellow, ERROR=red)
- File logs use plain format without colors
- Third-party loggers (SQLAlchemy, uvicorn) are configured to use the same format
- SQLAlchemy query logging is disabled by default (set `detailed_logs=true` for SQL logs)

## Adding New Features

### 1. Create Model
```python
# model/product.py
from sqlalchemy import Table, Column, Integer, String
from config.database_config import db

products = Table(
    'products',
    db.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(100), nullable=False),
    # ... more columns
)
```

### 2. Create Schemas (DTOs)
```python
# schema/product.py
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    # ... more fields

class ProductResponse(BaseModel):
    id: int
    name: str
    # ... more fields
```

### 3. Create Repository
```python
# repository/product_repository.py
from sqlalchemy import select, insert
from model.product import products

class ProductRepository:
    @staticmethod
    def get_all(conn):
        stmt = select(products)
        result = conn.execute(stmt)
        return [dict(row._mapping) for row in result.fetchall()]
    
    @staticmethod
    def create(conn, product_data):
        stmt = insert(products).values(**product_data)
        result = conn.execute(stmt)
        conn.commit()
        return result.lastrowid
```

### 4. Create Service
```python
# service/product_service.py
from repository.product_repository import ProductRepository

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def get_products(self, conn):
        return self.repository.get_all(conn)
    
    def create_product(self, conn, product_data):
        return self.repository.create(conn, product_data)
```

### 5. Create Controller
```python
# controller/product_controller.py
from fastapi import APIRouter, Depends
from config.database_config import get_db_connection
from service.product_service import ProductService
from schema.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
product_service = ProductService()

@router.get("/", response_model=list[ProductResponse])
def get_products(conn = Depends(get_db_connection)):
    return product_service.get_products(conn)

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, conn = Depends(get_db_connection)):
    product_id = product_service.create_product(conn, product.dict())
    return {"id": product_id, **product.dict()}
```

### 6. Register Router in main.py
```python
from controller.product_controller import router as product_router
app.include_router(product_router, prefix=config.api_prefix)
```

## Development Tips

- The database schema is automatically created on startup
- Use `DEBUG=true` for FastAPI debug mode
- Use `LOG_LEVEL=DEBUG` and `DETAILED_LOGS=true` for detailed logging including SQL queries
- Password hashing uses SHA-256 (consider bcrypt for production)
- Connection pooling is configured with 10 base connections, 20 max overflow
- All timestamps use UTC
- OpenAPI schema is auto-generated to `openapi.json` on startup
- Application banner displays on startup with configuration summary
