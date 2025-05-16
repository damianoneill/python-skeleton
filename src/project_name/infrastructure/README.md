# Infrastructure Layer

## Concept

The infrastructure layer contains all the technical details and implementations of interfaces defined in inner layers. It's where frameworks, databases, and external integrations reside.

## Responsibilities in REST API Context

- Configure and run the FastAPI application
- Set up database connections and ORM
- Implement HTTP clients for external APIs
- Configure logging, monitoring, and observability
- Manage technical concerns like authentication and caching

## What Does NOT Belong Here

- Business logic or rules
- Application flow control
- Domain entities or value objects
- Use case orchestration
- Interface definitions

## Example Concepts

### FastAPI Application Configuration

Setting up the FastAPI application:

```python
def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Customer API",
        description="API for customer management",
        version="1.0.0"
    )

    # Configure middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup error handlers
    register_exception_handlers(app)

    # Register routes
    register_routes(app)

    # Dependency injection setup
    setup_di(app)

    return app
```

### Route Configuration

Registering FastAPI routes with controllers, using Pydantic v2 models:

```python
def register_routes(app: FastAPI) -> None:
    """Register API routes"""

    # Create dependencies
    customer_controller = create_customer_controller()

    # Customer routes
    @app.post("/api/customers", response_model=CustomerResponse, status_code=201)
    async def register_customer(request: CustomerRegistrationRequest):
        return customer_controller.register_customer(request)

    @app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
    async def get_customer(customer_id: str):
        return customer_controller.get_customer(customer_id)

    # More routes...
```

### API Models for Error Handling

Defining structured error responses with Pydantic v2:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class ErrorDetail(BaseModel):
    """Error detail for field validation errors"""
    field: str
    message: str

class ErrorResponse(BaseModel):
    """Standardized error response format"""
    code: str
    message: str
    details: Optional[List[ErrorDetail]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed",
                    "details": [
                        {
                            "field": "email",
                            "message": "Invalid email format"
                        }
                    ]
                }
            ]
        }
    }
```

### Database Configuration

Setting up database connection and ORM:

```python
def get_session_factory():
    """Create database engine and session factory"""
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DB_ECHO,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW
    )

    session_factory = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    return session_factory

class CustomerModel(Base):
    """SQLAlchemy model for customers table"""
    __tablename__ = "customers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

### External API Client

Implementing HTTP clients for external services:

```python
def create_email_client():
    """Create and configure email client"""
    return EmailClient(
        api_key=settings.EMAIL_API_KEY,
        sender=settings.EMAIL_SENDER,
        base_url=settings.EMAIL_API_URL
    )

class EmailClient:
    """Client for email service API"""

    def __init__(self, api_key: str, sender: str, base_url: str):
        self.api_key = api_key
        self.sender = sender
        self.base_url = base_url
        self.session = httpx.AsyncClient(
            base_url=base_url,
            timeout=10.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        )

    async def send_message(self, recipient: str, subject: str, body: str) -> None:
        """Send email message"""
        payload = {
            "from": self.sender,
            "to": recipient,
            "subject": subject,
            "content": body
        }

        response = await self.session.post("/send", json=payload)
        response.raise_for_status()
```

## Components

- **Framework Configuration**: FastAPI app setup, middleware
- **Database Connection**: SQLAlchemy engine, session management
- **External API Clients**: HTTP clients for third-party services
- **Security Implementation**: Authentication, authorization
- **Technical Services**: Caching, messaging, file storage

## Guidelines for Clean Infrastructure Design

1. **Isolation** - Keep infrastructure concerns isolated from business logic

2. **Configuration management** - Externalize configuration through environment variables

3. **Error handling** - Implement proper error handling for external services

4. **Resource management** - Properly manage connections and resources

5. **Observability** - Ensure logging, metrics, and tracing
