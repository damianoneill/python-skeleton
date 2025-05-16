# Clean Architecture Concepts

This document explains the Clean Architecture approach used in this project.

## Overview

Clean Architecture creates a separation of concerns by dividing software into concentric layers. Each layer has a specific responsibility and a rule: dependencies only point inward. This ensures that business logic remains independent of delivery mechanisms and external systems.

## Request Flow Through Layers

Consider a RESTful endpoint that fetches data from multiple sources:

1. **Infrastructure Layer** (Outermost)
   - FastAPI route receives the HTTP request
   - Request details are extracted and passed to the adapter layer

2. **Adapter Layer**
   - Converts the HTTP request into a format suitable for the use case
   - Validates incoming data according to API contracts
   - Calls the appropriate use case with transformed data

3. **Use Case Layer**
   - Orchestrates the steps needed to fulfill the request
   - Applies business rules and makes decisions
   - Uses domain entities to execute core business logic
   - Calls repositories and services defined in domain layer

4. **Domain Layer** (Innermost)
   - Contains entities with business logic
   - Repositories define interfaces for data access
   - Service interfaces define external operation contracts
   - Enforces business invariants and rules

5. **Back through layers**
   - Domain layer returns entities or results to use case
   - Use case transforms results for external consumption
   - Adapter layer converts to HTTP response format
   - Infrastructure layer delivers the response via FastAPI

## Layer Responsibilities in REST Context

### Domain Layer

The domain layer remains completely unaware of REST APIs, FastAPI, or databases:

- Defines business entities like `Customer`, `Order`, `Product`
- Contains business logic and validation rules
- Defines repository interfaces for data access
- Defines service interfaces for external operations
- Has no dependencies on other layers or frameworks

### Use Case Layer

The use case layer orchestrates operations but remains independent of delivery mechanisms:

- Implements application flows like "Create Order" or "Process Payment"
- Coordinates between multiple domain entities
- Uses repository and service interfaces to access data and external systems
- Transforms between domain entities and DTOs
- Enforces application-specific business rules

### Adapter Layer

The adapter layer bridges between use cases and external interfaces:

- Converts between HTTP requests and use case inputs
- Transforms use case outputs into HTTP responses
- Implements repositories and services defined in inner layers
- Maps between domain models and external formats
- Handles API-specific concerns like pagination, filtering, sorting

### Infrastructure Layer

The infrastructure layer contains technical implementations:

- FastAPI application and route definitions
- Database connections and ORM configurations
- External API clients for third-party services
- Logging, monitoring, and configuration
- Framework-specific code

## Data Transfer Objects with Pydantic v2

In Clean Architecture, DTOs are used to transfer data between layers while maintaining layer isolation. Pydantic v2 offers significant benefits for implementing DTOs:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class CustomerDTO(BaseModel):
    """DTO for customer data moving between layers"""
    id: str
    name: str
    email: str
    verified: bool = False
    created_at: datetime

    model_config = {
        "frozen": True  # Makes the DTO immutable
    }

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format"""
        if '@' not in v:
            raise ValueError("Invalid email format")
        return v
```

With these DTOs:

- Domain entities remain unaffected by presentation concerns
- Input validation is handled consistently
- Schema documentation is automatic
- Serialization/deserialization is built-in

## Data Flow for External Integrations

For an API that fetches data from multiple sources:

1. **External Request → Internal Processing**
   - Infrastructure: FastAPI route receives request
   - Adapter: Converts request to use case input
   - Use Case: Determines required data sources
   - Domain: Defines repository interfaces for data access

2. **Internal → External Systems**
   - Use Case: Calls repository methods
   - Adapter: Repository implementations perform external calls
   - Infrastructure: Database clients and API clients execute requests

3. **External Data → Response**
   - Infrastructure: Receives raw data from external systems
   - Adapter: Converts raw data to domain entities
   - Use Case: Processes and combines domain entities
   - Adapter: Transforms results to response format
   - Infrastructure: Delivers HTTP response

## Maintaining Layer Boundaries

To maintain clean boundaries between layers:

1. **Interfaces for Outward Communication**
   - Domain defines repository interfaces implemented by adapters
   - Use cases define service interfaces implemented by adapters

2. **DTOs for Layer Crossing**
   - Data Transfer Objects carry data between layers
   - Prevent domain entities from leaking to outer layers

3. **Dependency Injection**
   - Outer layers provide implementations to inner layers
   - Dependencies flow in the opposite direction of control

4. **Unidirectional Dependencies**
   - Domain has no imports from other layers
   - Use cases only import from domain
   - Adapters import from use cases and domain
   - Infrastructure imports from all other layers

## Testing Strategy

Clean Architecture enables effective testing strategies:

1. **Domain Layer Tests**
   - Pure unit tests without mocks
   - Focus on business logic correctness
   - Fast and reliable

2. **Use Case Layer Tests**
   - Unit tests with mocked repositories and services
   - Verify orchestration logic
   - Test business flow correctness

3. **Adapter Layer Tests**
   - Test correct transformation of data
   - Verify repository implementations
   - Mock external dependencies

4. **Infrastructure Layer Tests**
   - Integration tests with actual databases or APIs
   - Test framework configuration
   - Verify external connectivity

5. **End-to-End Tests**
   - Test complete flows through all layers
   - Verify system behavior as a whole
   - Complement unit and integration tests
