# Adapter Layer

## Concept

The adapter layer converts between the formats needed by external systems and the formats used by the use cases. It acts as a bridge between the application core and external concerns.

## Responsibilities in REST API Context

- Transform HTTP requests into use case inputs
- Convert use case outputs into HTTP responses
- Implement repositories defined in domain layer
- Map between API models and domain entities
- Handle API-specific concerns (pagination, filtering)

## What Does NOT Belong Here

- Business rules or logic
- Core domain entities
- Database connection details
- Framework configuration
- Application flow orchestration

## Example Concepts

### API Models

Pydantic models for API request/response validation:

```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional

class CustomerRegistrationRequest(BaseModel):
    """API request model for customer registration"""
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }

class CustomerResponse(BaseModel):
    """API response model for customer data"""
    id: str
    name: str
    email: str
    verified: bool
    created_at: datetime
```

### Error Response Models

Standardized error responses with Pydantic v2:

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

def create_validation_error(message: str, details: List[ErrorDetail]) -> ErrorResponse:
    """Factory method for validation errors"""
    return ErrorResponse(
        code="VALIDATION_ERROR",
        message=message,
        details=details
    )
```

### Controllers/Handlers

API handlers that map between HTTP and use cases, using Pydantic models:

```python
class CustomerController:
    """Controller handling customer-related endpoints"""

    def __init__(self, customer_service: CustomerService):
        self.customer_service = customer_service

    def register_customer(self, request: CustomerRegistrationRequest) -> Union[CustomerResponse, ErrorResponse]:
        """Handle customer registration endpoint"""
        # Map API request to command
        try:
            command = RegisterCustomerCommand(
                name=request.name,
                email=request.email,
                password=request.password
            )
        except ValidationError as e:
            # Convert Pydantic validation errors to API response
            details = [
                ErrorDetail(field=error["loc"][0], message=error["msg"])
                for error in e.errors()
            ]
            return create_validation_error("Validation failed", details)

        # Execute use case
        result = self.customer_service.register_customer(command)

        # Handle result
        if result.is_success():
            customer_dto = result.value
            return CustomerResponse(
                id=customer_dto.id,
                name=customer_dto.name,
                email=customer_dto.email,
                verified=customer_dto.verified,
                created_at=customer_dto.created_at
            )
        else:
            return ErrorResponse(
                code="VALIDATION_ERROR",
                message="Validation failed",
                details=[ErrorDetail(field=field, message=msg) for field, msg in result.error]
            )

    def get_customer(self, customer_id: str) -> Union[CustomerResponse, ErrorResponse]:
        """Handle get customer endpoint"""
        customer_dto = self.customer_service.get_customer(customer_id)
        if not customer_dto:
            return ErrorResponse(
                code="NOT_FOUND",
                message=f"Customer with ID {customer_id} not found"
            )

        return CustomerResponse(
            id=customer_dto.id,
            name=customer_dto.name,
            email=customer_dto.email,
            verified=customer_dto.verified,
            created_at=customer_dto.created_at
        )
```

### Repository Implementations

Implementations of domain repository interfaces:

```python
class SQLAlchemyCustomerRepository(CustomerRepository):
    """SQLAlchemy implementation of the CustomerRepository interface"""

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def find_by_id(self, id: str) -> Optional[Customer]:
        """Find customer by ID"""
        with self.session_factory() as session:
            customer_model = session.query(CustomerModel).filter(CustomerModel.id == id).first()
            if not customer_model:
                return None
            return self._to_entity(customer_model)

    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find customer by email"""
        with self.session_factory() as session:
            customer_model = session.query(CustomerModel).filter(CustomerModel.email == email).first()
            if not customer_model:
                return None
            return self._to_entity(customer_model)

    def save(self, customer: Customer) -> None:
        """Save customer to database"""
        with self.session_factory() as session:
            customer_model = CustomerModel(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                verified=customer.verified,
                created_at=customer.created_at
            )
            session.add(customer_model)
            session.commit()

    def _to_entity(self, model: CustomerModel) -> Customer:
        """Convert database model to domain entity"""
        customer = Customer(
            id=model.id,
            name=model.name,
            email=model.email
        )
        customer.verified = model.verified
        customer._created_at = model.created_at  # Using protected field to set readonly property
        return customer
```

### Service Implementations

Implementations of domain service interfaces:

```python
class EmailNotificationService(NotificationService):
    """Implementation of notification service using email"""

    def __init__(self, email_client):
        self.email_client = email_client

    def send_email(self, to: str, subject: str, content: str) -> bool:
        """Send email notification"""
        try:
            self.email_client.send_message(
                recipient=to,
                subject=subject,
                body=content
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_sms(self, to: str, message: str) -> bool:
        """Send SMS notification"""
        # Not implemented in this service
        logger.warning("SMS notifications not supported by EmailNotificationService")
        return False
```

## Components

- **API Controllers**: Handle routing requests to use cases
- **Presenters**: Format use case outputs for HTTP responses
- **Repository Implementations**: Connect domain interfaces to data sources
- **External Service Clients**: Implement domain service interfaces
- **Data Mappers**: Convert between external and internal formats

## Guidelines for Clean Adapter Design

1. **Separation of concerns** - Each adapter should have a single responsibility

2. **Clean mappings** - Create clear transformations between formats

3. **Implementation hiding** - Hide implementation details behind interfaces

4. **Error translation** - Map between domain/application errors and external formats

5. **Independence** - Each adapter should be independent of other adapters
