# FastAPI Starter Backend

A production-ready FastAPI starter template with clean architecture, SQLAlchemy ORM, and support for multiple databases (SQLite, MySQL, Oracle).

## Table of Contents

- [About](#about)
- [Features](#features)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Management](#database-management)
- [Development Guide](#development-guide)
  - [Adding Models](#adding-models)
  - [Adding Schemas](#adding-schemas)
  - [Adding Repositories](#adding-repositories)
  - [Adding Services](#adding-services)
  - [Adding Controllers](#adding-controllers)
- [Logging Configuration](#logging-configuration)
- [OpenAPI Schema Generation](#openapi-schema-generation)
- [Main Application Entry Point](#main-application-entry-point)

---

## About

This is a FastAPI starter template following clean architecture principles with a clear separation of concerns. It implements a layered architecture inspired by Spring Boot:

- **Controller Layer**: REST API endpoints
- **Service Layer**: Business logic
- **Repository Layer**: Data access
- **Model Layer**: ORM entities
- **Schema Layer**: Request/Response DTOs (Data Transfer Objects)

The architecture uses SQLAlchemy ORM for database operations, supporting SQLite (development), MySQL, and Oracle databases.

---

## Features

- **Clean Architecture**: Layered design with clear separation of concerns (Controller → Service → Repository → Model)
- **SQLAlchemy ORM**: Modern ORM with type hints and Spring Boot-style entity patterns
- **Multi-Database Support**: SQLite, MySQL, and Oracle with easy switching
- **Auto-Discovery Models**: Add new models without editing database configuration
- **Centralized Configuration**: TOML-based config with environment variable overrides
- **Advanced Logging**: Separate application and audit logs with rotation support
- **Request ID Tracking**: UUID-based request tracing for debugging
- **Password Hashing**: Secure bcrypt password hashing
- **CORS Support**: Configurable CORS middleware
- **OpenAPI Generation**: Automatic OpenAPI 3.0 schema generation
- **Hot Reload**: Development server with auto-reload on code changes
- **Type Safety**: Full type hints throughout the codebase

---

## Environment Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation Steps

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd FastApiStarterBackend
```

#### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
```

**Linux/macOS:**
```bash
python3 -m venv .venv
```

#### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Start the Server

```bash
python src/main.py
```

The server will start on `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative Docs: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/`

---

## Project Structure

```
FastApiStarterBackend/
├── src/
│   ├── main.py                      # Application entry point
│   ├── common/                      # Shared utilities
│   │   ├── base.py                  # SQLAlchemy Base class
│   │   └── util/                    # Utility functions
│   │       ├── banner.py            # Startup banner
│   │       └── openapi_generator.py # OpenAPI schema generator
│   ├── config/                      # Configuration modules
│   │   ├── app_config.py            # Application configuration
│   │   ├── database_config.py       # Database configuration
│   │   └── log_config.py            # Logging configuration
│   ├── controller/                  # REST API controllers
│   │   ├── __init__.py              # Export routers
│   │   └── user_controller.py       # User endpoints
│   ├── service/                     # Business logic layer
│   │   ├── __init__.py
│   │   └── user_service.py          # User business logic
│   ├── repository/                  # Data access layer
│   │   ├── __init__.py
│   │   └── user_repository.py       # User data access
│   ├── model/                       # ORM entity models
│   │   ├── __init__.py              # Export models
│   │   └── user.py                  # User entity
│   └── schema/                      # Pydantic schemas (DTOs)
│       ├── __init__.py
│       ├── common.py                # Common schemas
│       └── user.py                  # User DTOs
├── logs/                            # Log files (auto-created)
│   ├── app.log                      # Application logs
│   ├── debug.log                    # Debug logs (when enabled)
│   └── audit.log                    # Request/response audit logs
├── deployment.toml                  # Configuration file
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
├── fastapi_db.sqlite                # SQLite database (auto-created)
└── openapi.json                     # Generated OpenAPI schema
```

---

## Configuration

### Configuration Files

The application uses two configuration sources:

1. **deployment.toml**: Main configuration file
2. **.env**: Environment variables (optional, takes precedence)

### deployment.toml Structure

```toml
[application]
app_name = "FastAPI Starter"
debug = false
api_prefix = "/api/v1"

[server]
host = "0.0.0.0"
port = 8000
reload = true

[cors]
origins = ["http://localhost:3000", "http://localhost:8080"]
allow_credentials = true
allow_methods = ["*"]
allow_headers = ["*"]

[database]
db_type = "sqlite"  # Options: "sqlite", "mysql", "oracle"
sqlite_file = "fastapi_db.sqlite"

# MySQL/Oracle settings
host = "localhost"
port = 3306
username = "${DB_USERNAME}"
password = "${DB_PASSWORD}"
database = "fastapi_db"
service_name = "ORCL"  # Oracle only

[logging]
log_level = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
log_to_file = true
log_dir = "logs"
detailed_logs = true
rotation_type = "both"  # "size", "time", or "both"
max_bytes = 10485760  # 10MB
backup_count = 5
rotation_when = "midnight"
rotation_interval = 1
rotation_backup_count = 30
```

### Environment Variables

Create a `.env` file in the project root for sensitive data:

```env
# Database credentials
DB_USERNAME=your_username
DB_PASSWORD=your_password

# Override any TOML setting
API_PREFIX=/api/v2
LOG_LEVEL=DEBUG
```

### Adding New Configuration Settings

#### Step 1: Add to deployment.toml

```toml
[application]
api_timeout = 30
```

#### Step 2: Add property to AppConfig (optional but recommended)

Edit `src/config/app_config.py`:

```python
@property
def api_timeout(self) -> int:
    """API request timeout in seconds"""
    return self.get("application", "api_timeout", 30)
```

#### Step 3: Use in your code

```python
from config.app_config import config

timeout = config.api_timeout
```

### Environment Variable Substitution

The configuration supports `${VAR_NAME}` syntax for environment variable substitution:

```toml
[database]
username = "${DB_USERNAME}"  # Replaced with value from environment
password = "${DB_PASSWORD}"
```

---

## Database Management

### Supported Databases

- **SQLite**: Default, no setup required (development)
- **MySQL**: Production-ready relational database
- **Oracle**: Enterprise database support

### Database Migrations with Alembic

This project uses **Alembic** for database migrations, allowing you to track and version schema changes over time.

#### Migration Files Location

- **Configuration**: `alembic.ini`
- **Migration Scripts**: `alembic/versions/`
- **Environment Setup**: `alembic/env.py`

#### Common Migration Commands

**Check current migration status:**
```bash
alembic current
```

**View migration history:**
```bash
alembic history --verbose
```

**Generate a new migration (auto-detect changes):**
```bash
alembic revision --autogenerate -m "Add status column to users"
```

**Apply migrations (upgrade to latest):**
```bash
alembic upgrade head
```

**Rollback one migration:**
```bash
alembic downgrade -1
```

**Rollback to specific revision:**
```bash
alembic downgrade <revision_id>
```

**Rollback all migrations:**
```bash
alembic downgrade base
```

**Show SQL without executing:**
```bash
alembic upgrade head --sql
```

#### Migration Workflow Example

**Scenario**: Add a `status` column to the `users` table.

**Step 1: Modify the Model**

Edit `src/model/user.py`:
```python
class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # NEW COLUMN
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now, nullable=False)
```

**Step 2: Generate Migration**
```bash
alembic revision --autogenerate -m "Add status column to users table"
```

Output:
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added column 'users.status'
Generating alembic/versions/20251129_1815-abc123def456_add_status_column_to_users_table.py ... done
```

**Step 3: Review Generated Migration**

Alembic creates a migration file in `alembic/versions/`. Always review before applying:

```python
def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('status', sa.String(length=20), nullable=False, server_default='active'))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'status')
    # ### end Alembic commands ###
```

**Step 4: Apply Migration**
```bash
alembic upgrade head
```

Output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, Add status column to users table
```

**Step 5: Verify**
```bash
alembic current
```

Output:
```
abc123def456 (head)
```

#### Manual Migration Creation

For complex changes, create an empty migration and write custom SQL:

```bash
alembic revision -m "Custom migration description"
```

Edit the generated file:
```python
def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
        CREATE INDEX idx_users_last_login ON users(last_login);
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP INDEX idx_users_last_login;
        ALTER TABLE users DROP COLUMN last_login;
    """)
```

#### Migration Best Practices

1. **Always Review Generated Migrations**: Auto-generated migrations may not always be perfect. Review before applying.

2. **Use Descriptive Messages**: 
   ```bash
   # Good
   alembic revision --autogenerate -m "Add user status and last_login columns"
   
   # Bad
   alembic revision --autogenerate -m "update"
   ```

3. **Test Migrations**: Test both `upgrade` and `downgrade` paths:
   ```bash
   alembic upgrade head
   alembic downgrade -1
   alembic upgrade head
   ```

4. **Add Default Values**: When adding non-nullable columns to tables with existing data:
   ```python
   op.add_column('users', sa.Column('status', sa.String(20), 
                 nullable=False, server_default='active'))
   ```

5. **Handle Data Migrations**: For data transformations, use `op.execute()`:
   ```python
   def upgrade() -> None:
       # Schema change
       op.add_column('users', sa.Column('full_name', sa.String(200)))
       
       # Data migration
       op.execute("""
           UPDATE users 
           SET full_name = first_name || ' ' || last_name
       """)
   ```

6. **Keep Migrations Small**: One logical change per migration makes rollbacks easier.

7. **Don't Edit Applied Migrations**: Once a migration is applied (especially in production), never edit it. Create a new migration instead.

#### Common Migration Scenarios

**Rename Column:**
```python
def upgrade():
    op.alter_column('users', 'user_name', new_column_name='username')

def downgrade():
    op.alter_column('users', 'username', new_column_name='user_name')
```

**Add Index:**
```python
def upgrade():
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
```

**Add Foreign Key:**
```python
def upgrade():
    op.create_foreign_key(
        'fk_orders_user_id', 
        'orders', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
```

**Change Column Type:**
```python
def upgrade():
    # SQLite doesn't support ALTER COLUMN, need to recreate table
    op.alter_column('users', 'age', type_=sa.SmallInteger())

def downgrade():
    op.alter_column('users', 'age', type_=sa.Integer())
```

#### Troubleshooting

**"Target database is not up to date":**
```bash
# Check current version
alembic current

# Upgrade to latest
alembic upgrade head
```

**"Can't locate revision identified by '<revision_id>'":**
- Ensure all migration files are in `alembic/versions/`
- Check for missing or deleted migration files

**Autogenerate doesn't detect changes:**
- Ensure model is imported in `model/__init__.py`
- Restart Python to clear cached imports
- Check that `target_metadata` is set in `alembic/env.py`

**Migration fails midway:**
```bash
# Mark migration as failed (doesn't rollback)
alembic stamp head

# Or manually rollback and fix
alembic downgrade -1
# Fix the migration script
alembic upgrade head
```

#### Initial Setup for Existing Database

If you have an existing database with tables already created:

**Step 1: Create initial migration without changes:**
```bash
alembic revision -m "Initial migration - existing schema"
```

**Step 2: Mark database as up-to-date without running migrations:**
```bash
alembic stamp head
```

This tells Alembic that your database is already at the latest version.

### Switching Databases

#### SQLite (Default)

```toml
[database]
db_type = "sqlite"
sqlite_file = "fastapi_db.sqlite"
```

No additional configuration needed.

#### MySQL

1. Install MySQL driver (already in requirements.txt):
```bash
pip install pymysql cryptography
```

2. Update deployment.toml:
```toml
[database]
db_type = "mysql"
host = "localhost"
port = 3306
username = "${DB_USERNAME}"
password = "${DB_PASSWORD}"
database = "fastapi_db"
```

3. Set environment variables:
```env
DB_USERNAME=your_mysql_user
DB_PASSWORD=your_mysql_password
```

#### Oracle

1. Install Oracle driver:
```bash
pip install cx-oracle
```

2. Update deployment.toml:
```toml
[database]
db_type = "oracle"
host = "localhost"
port = 1521
username = "${DB_USERNAME}"
password = "${DB_PASSWORD}"
service_name = "ORCL"
```

3. Install Oracle Instant Client (required for cx_Oracle)

### Adding Support for Other Databases

Edit `src/config/database_config.py` and add a new connection URL builder:

```python
elif db_type == "postgresql":
    url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
```

---

## Development Guide

### Adding Models

Models are SQLAlchemy ORM entities that map to database tables.

#### Step 1: Create Model File

Create `src/model/product.py`:

```python
"""
Product Model - SQLAlchemy ORM Entity Definition
"""

from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from common.base import Base


def utc_now() -> datetime:
    """Return current UTC time with timezone info"""
    return datetime.now(timezone.utc)


class Product(Base):
    """Product entity"""
    __tablename__ = 'products'
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Product details
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, 
        onupdate=utc_now, 
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}')>"
```

#### Step 2: Register Model

Edit `src/model/__init__.py`:

```python
"""
Database Models Package
"""

from model.user import User
from model.product import Product

__all__ = ["User", "Product"]
```

#### Step 3: Run Application

The table will be created automatically on startup due to auto-discovery.

**Key Points:**
- Always inherit from `common.base.Base`
- Use `Mapped[type]` for type hints
- Add `__tablename__` attribute
- Use `utc_now()` for timezone-aware timestamps
- Import and export in `model/__init__.py`

---

### Adding Schemas

Schemas are Pydantic models used for request validation and response serialization (DTOs).

#### Step 1: Create Schema File

Create `src/schema/product.py`:

```python
"""
Product Schemas - Request and Response DTOs
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    """Base product schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    description: Optional[str] = Field(None, max_length=500, description="Product description")
    price: float = Field(..., gt=0, description="Product price")
    stock: int = Field(default=0, ge=0, description="Stock quantity")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "description": "High-performance laptop",
                "price": 999.99,
                "stock": 50
            }
        }
    )


class ProductUpdate(BaseModel):
    """Schema for updating product information"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)
```

#### Step 2: Export Schema

Edit `src/schema/__init__.py`:

```python
from schema.product import ProductCreate, ProductUpdate, ProductResponse

__all__ = [..., "ProductCreate", "ProductUpdate", "ProductResponse"]
```

**Key Points:**
- Use Pydantic `BaseModel`
- Add validation with `Field()`
- Use `ConfigDict(from_attributes=True)` for response schemas
- Provide examples for documentation
- Separate Create, Update, and Response schemas

---

### Adding Repositories

Repositories handle database operations (Data Access Layer).

#### Step 1: Create Repository File

Create `src/repository/product_repository.py`:

```python
"""
Product Repository - Data Access Layer using SQLAlchemy ORM
"""

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from model.product import Product
from schema.product import ProductCreate, ProductUpdate


class ProductRepository:
    """Repository for product data access operations"""
    
    def __init__(self, session: Session):
        """Initialize repository with database session"""
        self.session = session
    
    def create(self, product: ProductCreate) -> Product:
        """Create a new product"""
        now = datetime.now(timezone.utc)
        product_entity = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            created_at=now,
            updated_at=now
        )
        self.session.add(product_entity)
        self.session.flush()
        return product_entity
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.session.get(Product, product_id)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Product]:
        """Get all products with pagination"""
        stmt = select(Product).offset(skip).limit(limit).order_by(Product.id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())
    
    def count(self) -> int:
        """Count total number of products"""
        stmt = select(func.count()).select_from(Product)
        result = self.session.execute(stmt)
        return result.scalar()
    
    def update(self, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        """Update product information"""
        product_entity = self.session.get(Product, product_id)
        if not product_entity:
            return None
        
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product_entity, key, value)
        
        product_entity.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return product_entity
    
    def delete(self, product_id: int) -> bool:
        """Delete product by ID"""
        product_entity = self.session.get(Product, product_id)
        if not product_entity:
            return False
        
        self.session.delete(product_entity)
        self.session.flush()
        return True
```

**Key Points:**
- Accept `Session` in constructor
- Use `session.flush()` instead of `commit()` (handled by dependency)
- Return entities, not dictionaries
- Use timezone-aware datetimes
- Add common CRUD operations

---

### Adding Services

Services contain business logic and orchestrate repositories.

#### Step 1: Create Service File

Create `src/service/product_service.py`:

```python
"""
Product Service - Business Logic Layer
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

from repository.product_repository import ProductRepository
from schema.product import ProductCreate, ProductUpdate, ProductResponse
from model.product import Product


class ProductService:
    """Service for product business logic"""
    
    def __init__(self, session: Session):
        """Initialize service with database session"""
        self.repository = ProductRepository(session)
        self.logger = logging.getLogger(__name__)
    
    def _entity_to_dto(self, product: Product) -> ProductResponse:
        """Convert Product entity to ProductResponse DTO"""
        return ProductResponse.model_validate(product)
    
    def create_product(self, product: ProductCreate) -> ProductResponse:
        """Create a new product"""
        self.logger.info(f"Creating new product: {product.name}")
        
        # Business validation
        if product.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Price must be greater than zero"
            )
        
        # Create product
        product_entity = self.repository.create(product)
        self.logger.info(f"Product created successfully with ID: {product_entity.id}")
        
        return self._entity_to_dto(product_entity)
    
    def get_product(self, product_id: int) -> ProductResponse:
        """Get product by ID"""
        self.logger.debug(f"Fetching product with ID: {product_id}")
        product_entity = self.repository.get_by_id(product_id)
        
        if not product_entity:
            self.logger.warning(f"Product not found with ID: {product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        return self._entity_to_dto(product_entity)
    
    def update_product(self, product_id: int, product_update: ProductUpdate) -> ProductResponse:
        """Update product information"""
        self.logger.info(f"Updating product with ID: {product_id}")
        
        existing_product = self.repository.get_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        updated_entity = self.repository.update(product_id, product_update)
        self.logger.info(f"Product updated successfully: {product_id}")
        
        return self._entity_to_dto(updated_entity)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID"""
        self.logger.info(f"Deleting product with ID: {product_id}")
        
        if not self.repository.get_by_id(product_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        
        success = self.repository.delete(product_id)
        self.logger.info(f"Product deleted successfully: {product_id}")
        return success
```

**Key Points:**
- Initialize repository in constructor
- Add business validation logic
- Use `_entity_to_dto()` for conversion
- Raise `HTTPException` for errors
- Add logging for important operations

---

### Adding Controllers

Controllers define REST API endpoints.

#### Step 1: Create Controller File

Create `src/controller/product_controller.py`:

```python
"""Product Controller - REST API Endpoints"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import logging

from config.database_config import get_db_session
from service.product_service import ProductService
from schema.product import ProductCreate, ProductUpdate, ProductResponse
from schema.common import MessageResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product"
)
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_db_session)
):
    """Create a new product"""
    logger.info(f"Creating product: {product.name}")
    product_service = ProductService(session)
    result = product_service.create_product(product)
    logger.info(f"Product created with ID: {result.id}")
    return result


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID"
)
def get_product(
    product_id: int,
    session: Session = Depends(get_db_session)
):
    """Get product by ID"""
    logger.debug(f"Fetching product: {product_id}")
    product_service = ProductService(session)
    return product_service.get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product"
)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: Session = Depends(get_db_session)
):
    """Update product information"""
    logger.info(f"Updating product: {product_id}")
    product_service = ProductService(session)
    return product_service.update_product(product_id, product_update)


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    summary="Delete product"
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete product by ID"""
    logger.info(f"Deleting product: {product_id}")
    product_service = ProductService(session)
    product_service.delete_product(product_id)
    return MessageResponse(
        message=f"Product with ID {product_id} deleted successfully",
        success=True
    )
```

#### Step 2: Register Router

Edit `src/controller/__init__.py`:

```python
"""
Controllers Package
Export all API routers
"""

from controller.user_controller import router as user_router
from controller.product_controller import router as product_router

__all__ = ["user_router", "product_router"]
```

#### Step 3: Add to Main Application

Edit `src/main.py`:

```python
from controller import user_router, product_router

# Register routers
app.include_router(user_router, prefix=config.api_prefix)
app.include_router(product_router, prefix=config.api_prefix)
```

**Key Points:**
- Use `APIRouter` for route grouping
- Add `prefix` and `tags` for organization
- Use `Depends(get_db_session)` for database access
- Specify `response_model` for automatic validation
- Add docstrings for API documentation
- Use appropriate HTTP status codes

---

## Logging Configuration

The application uses Python's built-in logging with advanced features.

### Log Files

- `logs/app.log`: All application logs
- `logs/debug.log`: Debug-level logs only (when log_level=DEBUG)
- `logs/audit.log`: HTTP request/response audit trail

### Configuration

Edit `deployment.toml`:

```toml
[logging]
log_level = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
log_to_file = true
log_dir = "logs"
detailed_logs = true  # Include file and line numbers

# Rotation settings
rotation_type = "both"  # "size", "time", or "both"

# Size-based rotation
max_bytes = 10485760  # 10MB
backup_count = 5

# Time-based rotation
rotation_when = "midnight"  # "S", "M", "H", "D", "midnight", "W0"-"W6"
rotation_interval = 1
rotation_backup_count = 30
```

### Adding Logs to Your Code

#### In Repository

```python
import logging

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)
    
    def create(self, product: ProductCreate) -> Product:
        self.logger.debug(f"Creating product: {product.name}")
        # ... logic ...
        self.logger.info(f"Product created with ID: {product_entity.id}")
        return product_entity
```

#### In Service

```python
import logging

class ProductService:
    def __init__(self, session: Session):
        self.repository = ProductRepository(session)
        self.logger = logging.getLogger(__name__)
    
    def create_product(self, product: ProductCreate) -> ProductResponse:
        self.logger.info(f"Creating new product: {product.name}")
        # ... business logic ...
        self.logger.warning("Stock is low")  # Warning
        self.logger.error("Failed to process")  # Error
        return result
```

#### In Controller

```python
import logging

logger = logging.getLogger(__name__)

@router.post("/")
def create_product(product: ProductCreate, session: Session = Depends(get_db_session)):
    logger.info(f"API: Creating product: {product.name}")
    # ... logic ...
    return result
```

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious errors

### Log Format

**Standard format:**
```
2024-01-01 10:30:45 | INFO | service.product_service | Creating new product: Laptop
```

**Detailed format (when detailed_logs=true):**
```
2024-01-01 10:30:45 | INFO | service.product_service:42 | Creating new product: Laptop
```

### Audit Logs

Request/response logs are automatically captured:

```
2024-01-01 10:30:45 | REQUEST | abc-123-def | GET /api/v1/products | Client: 127.0.0.1
2024-01-01 10:30:46 | RESPONSE | abc-123-def | GET /api/v1/products | Status: 200 | Time: 0.045s
```

Each log includes the request ID for correlation.

---

## OpenAPI Schema Generation

The application automatically generates an OpenAPI 3.0 schema file on startup.

### Generated File

- **Location**: `openapi.json` (project root)
- **Format**: JSON
- **Standard**: OpenAPI 3.0

### How It Works

The schema is generated in `src/main.py` during application startup:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print_banner()
    init_db()
    
    # Generate OpenAPI schema file
    generate_openapi_file(app, output_path="openapi.json")
    
    yield
    
    # Shutdown
    db.close()
```

### Ensuring Proper Schema Generation

#### 1. Add Response Models

Always specify `response_model` in your endpoints:

```python
@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Get product by ID"""
    pass
```

#### 2. Add Docstrings

Function docstrings become endpoint descriptions:

```python
@router.post("/products/")
def create_product(product: ProductCreate):
    """
    Create a new product with the following information:
    
    - **name**: Product name (required)
    - **price**: Product price (required, must be positive)
    - **stock**: Initial stock quantity (optional)
    """
    pass
```

#### 3. Use Pydantic Schema Examples

Add examples to your schemas:

```python
class ProductCreate(BaseModel):
    name: str
    price: float
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "stock": 50
            }
        }
    )
```

#### 4. Add Field Descriptions

Use `Field()` to add descriptions:

```python
class ProductCreate(BaseModel):
    name: str = Field(..., description="Product name", min_length=1, max_length=100)
    price: float = Field(..., description="Product price in USD", gt=0)
    stock: int = Field(default=0, description="Available stock quantity", ge=0)
```

#### 5. Use Status Codes

Specify status codes for different responses:

```python
@router.post(
    "/products/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Invalid product data"},
        409: {"description": "Product already exists"}
    }
)
def create_product(product: ProductCreate):
    pass
```

### Customizing API Metadata

Edit `src/main.py`:

```python
app = FastAPI(
    title="My API",
    description="Comprehensive API description with **markdown** support",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
        "url": "https://example.com/support"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)
```

### Using the Generated Schema

The `openapi.json` file can be used with:

- **Swagger UI**: Import into Swagger Editor
- **Postman**: Import as OpenAPI 3.0 collection
- **Code Generators**: Generate client SDKs
- **API Gateways**: Configure API management platforms
- **Documentation**: Generate static documentation

---

## Main Application Entry Point

The `src/main.py` file is the application entry point that orchestrates all components.

### Structure

```python
# 1. Imports
from fastapi import FastAPI, Request
from config.app_config import config
from controller import user_router

# 2. Logging Setup
setup_logging(...)
audit_logger = setup_audit_logger(...)
logger = logging.getLogger(__name__)

# 3. Lifespan Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print_banner()
    init_db()
    generate_openapi_file(app)
    yield
    # Shutdown
    db.close()

# 4. FastAPI App Creation
app = FastAPI(
    title=config.app_name,
    version="1.0.0",
    lifespan=lifespan
)

# 5. Middleware
app.add_middleware(CORSMiddleware, ...)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    # Request ID tracking
    pass

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Request/response logging
    pass

# 6. Router Registration
app.include_router(user_router, prefix=config.api_prefix)

# 7. Health Check
@app.get("/")
def health_check():
    return {"status": "healthy"}

# 8. Development Server
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
```

### Key Components

#### Lifespan Manager

Handles startup and shutdown events:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    init_db()
    yield
    # Shutdown: Cleanup resources
    db.close()
```

#### Middleware

Middleware executes for every request:

**Request ID Tracking:**
```python
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

**Request Logging:**
```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    audit_logger.info(f"REQUEST | {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    audit_logger.info(f"RESPONSE | Status: {response.status_code} | Time: {process_time:.3f}s")
    return response
```

#### Router Registration

Controllers are registered with URL prefixes:

```python
app.include_router(user_router, prefix="/api/v1")
# Results in: /api/v1/users/...
```

#### Development Server

For local development:

```python
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=config.server_host,
        port=config.server_port,
        reload=True,  # Auto-reload on code changes
        reload_excludes=["**/logs/**", "**/*.log"]
    )
```

### Execution Order

1. Import statements execute
2. Logging is configured
3. Application instance is created
4. Middleware is registered (in order)
5. Routers are registered
6. Lifespan startup events trigger
   - Banner prints
   - Database initializes
   - OpenAPI schema generates
7. Server starts listening
8. On shutdown, lifespan shutdown events trigger

---

## Additional Resources

### API Documentation

- Interactive API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

### Best Practices

1. **Always use type hints**: Enables better IDE support and validation
2. **Use dependency injection**: Leverage FastAPI's `Depends()` for clean code
3. **Separate concerns**: Keep controllers thin, business logic in services
4. **Add logging**: Log important operations for debugging
5. **Use Pydantic validation**: Define schemas with proper validation rules
6. **Write docstrings**: Automatically generates API documentation
7. **Use timezone-aware datetimes**: Prevents timezone-related bugs
8. **Handle exceptions**: Raise appropriate HTTPExceptions with status codes

### Common Issues

**Import errors:**
- Ensure virtual environment is activated
- Check all dependencies are installed

**Database connection errors:**
- Verify database credentials in `.env`
- Check database server is running
- Confirm correct `db_type` in `deployment.toml`

**Port already in use:**
- Change port in `deployment.toml`
- Or kill process using the port

**Module not found:**
- Run from project root directory
- Check `PYTHONPATH` includes project root

---

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please refer to the project repository.
