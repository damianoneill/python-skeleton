# Use Case Layer

## Concept

The use case layer implements application-specific business flows. It orchestrates domain objects to accomplish specific tasks while remaining independent of delivery mechanisms.

## Responsibilities in REST API Context

- Implement operations exposed by the API
- Coordinate between multiple domain entities
- Apply application-specific business rules
- Transform between domain entities and DTOs
- Delegate data access and external operations to repositories and services

## What Does NOT Belong Here

- HTTP-specific logic or models
- Database or ORM details
- Framework dependencies
- Third-party API clients
- Direct references to infrastructure

## Example Concepts

### Data Transfer Objects (DTOs)

DTOs define the data structures for communication with outer layers, using Pydantic for validation:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CustomerDTO(BaseModel):
    """Data structure for transferring customer information"""
    id: str
    name: str
    email: str
    verified: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, customer: Customer) -> "CustomerDTO":
        return cls(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            verified=customer.verified,
            created_at=customer.created_at
        )
```

### Command Objects

Commands encapsulate all information needed for a specific operation:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List

class RegisterCustomerCommand(BaseModel):
    """Command to register a new customer"""
    name: str
    email: str
    password: str

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name is required")
        return v

    @field_validator('email')
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        if not v or '@' not in v:
            raise ValueError("Valid email is required")
        return v

    @field_validator('password')
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

### Use Case Services with Pydantic v2

Services that implement specific application use cases, leveraging Pydantic validation:

```python
from typing import Optional, Union, List, Tuple
from pydantic import ValidationError
from uuid import uuid4

# Result types to handle success/failure
class Success(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def is_success(self) -> bool:
        return True

class Failure:
    def __init__(self, error: List[Tuple[str, str]]):
        self.error = error

    def is_success(self) -> bool:
        return False

Result = Union[Success[T], Failure]

class CustomerService:
    """Service implementing customer-related use cases"""

    def __init__(self,
                 customer_repo: CustomerRepository,
                 notification_service: NotificationService):
        self.customer_repo = customer_repo
        self.notification_service = notification_service

    def register_customer(self, cmd: RegisterCustomerCommand) -> Result[CustomerDTO, List[Tuple[str, str]]]:
        """Register a new customer use case"""
        # Command is already validated by Pydantic

        # Check if customer already exists
        existing = self.customer_repo.find_by_email(cmd.email)
        if existing:
            return Failure([("email", "Email already registered")])

        # Create domain entity
        customer_id = str(uuid4())
        customer = Customer(customer_id, cmd.name, cmd.email)

        # Save to repository
        self.customer_repo.save(customer)

        # Send notification
        self.notification_service.send_email(
            customer.email,
            "Welcome to our service",
            f"Hi {customer.name}, thanks for registering!"
        )

        # Return DTO
        return Success(CustomerDTO.from_entity(customer))
```

## Flow Example

For an API endpoint fetching customer orders:

1. Receive input DTO with customer ID and filters
2. Validate input against application rules
3. Call customer and order repositories to fetch data
4. Apply business logic (permissions, calculations)
5. Transform domain entities to output DTOs
6. Return result to adapter layer

## Guidelines for Clean Use Case Design

1. **Single responsibility** - Each use case should focus on a specific application flow

2. **Input/output transformation** - Define clear DTOs for input and output

3. **Dependency inversion** - Depend on abstractions (interfaces) not implementations

4. **Error handling** - Use consistent error handling patterns

5. **Validation** - Validate inputs early before proceeding with business logic
