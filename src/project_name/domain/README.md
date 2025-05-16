# Domain Layer

## Concept

The domain layer represents the core business concepts independent of any external systems, frameworks, or use cases. It's the most stable layer, containing entities, business rules, and interface definitions.

## Responsibilities in REST API Context

- Define business entities and value objects
- Implement core business logic within entities
- Define repository interfaces for data access
- Define service interfaces for external operations
- Enforce business invariants and rules

## What Does NOT Belong Here

- HTTP-specific concepts or models
- Database models or query logic
- External API client details
- FastAPI dependencies or routes
- Any reference to outer layers

## Core Domain Concepts

The domain layer consists of several key building blocks from Domain-Driven Design:

1. **Entities**: Objects with identity that persists through time (e.g., `Customer`, `Order`)
2. **Value Objects**: Immutable objects with no identity (e.g., `Address`, `Money`)
3. **Aggregates**: Clusters of entities and value objects with consistency boundaries
4. **Domain Events**: Objects capturing significant occurrences in the domain
5. **Repository Interfaces**: Abstractions for data access
6. **Domain Services**: Behavior that doesn't belong to a specific entity

## Example Concepts

### Entities

Domain entities contain business logic and identity:

```python
class Customer:
    def __init__(self, id: str, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
        self.verified = False
        self.created_at = datetime.now()

    def verify_email(self) -> None:
        # Business logic for email verification
        self.verified = True

    def update_details(self, name: str = None, email: str = None) -> None:
        # Business logic for updating details
        if name:
            self.name = name
        if email:
            self.email = email
            self.verified = False
```

### Value Objects

Immutable objects that describe aspects of the domain, optionally using Pydantic for immutability:

```python
from pydantic import BaseModel, Field
from decimal import Decimal

class Address(BaseModel):
    """Value object representing a physical address"""
    street: str
    city: str
    post_code: str
    country: str

    model_config = {
        "frozen": True  # Makes the model immutable
    }

class Money(BaseModel):
    """Value object representing an amount of money in a specific currency"""
    amount: Decimal
    currency: str

    model_config = {
        "frozen": True
    }

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add money in {self.currency} to {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot subtract money in {other.currency} from {self.currency}")
        return Money(amount=self.amount - other.amount, currency=self.currency)
```

### Aggregates

Clusters of entities and value objects treated as a single unit with defined boundaries:

```python
from enum import Enum
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

class OrderStatus(Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem:
    """Entity within the Order aggregate"""
    def __init__(self, order_id: str, product_id: str, quantity: int, unit_price: Decimal):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price

class OrderError(Exception):
    """Domain exception for Order-related errors"""
    pass

class Order:
    """Order aggregate root"""
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items = []  # OrderItem entities
        self.status = OrderStatus.DRAFT
        self.shipping_address = None  # Address value object
        self.billing_address = None   # Address value object
        self.created_at = datetime.now()

    def add_item(self, product_id: str, quantity: int, unit_price: Decimal) -> None:
        """Add item to order, enforcing business rules"""
        # Business rule: Cannot add items to completed orders
        if self.status not in [OrderStatus.DRAFT, OrderStatus.PENDING]:
            raise OrderError("Cannot modify a completed order")

        # Business rule: Quantity must be positive
        if quantity <= 0:
            raise OrderError("Quantity must be positive")

        # Check if product already exists in order
        for item in self.items:
            if item.product_id == product_id:
                # Update existing item
                item.quantity += quantity
                return

        # Add new item
        item = OrderItem(
            order_id=self.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )
        self.items.append(item)

    def calculate_total(self) -> Decimal:
        """Calculate order total"""
        return sum(item.quantity * item.unit_price for item in self.items)

    def submit(self) -> None:
        """Submit the order, enforcing business rules"""
        # Business rule: Cannot submit an empty order
        if not self.items:
            raise OrderError("Cannot submit an empty order")

        # Business rule: Shipping address required
        if not self.shipping_address:
            raise OrderError("Shipping address is required")

        # Business rule: Billing address required
        if not self.billing_address:
            raise OrderError("Billing address is required")

        self.status = OrderStatus.PENDING
```

### Repository Interfaces

Repository interfaces defined here would be implemented in adapter layer:

```python
from typing import List, Optional, Protocol

class CustomerRepository(Protocol):
    def find_by_id(self, id: str) -> Optional[Customer]: ...
    def find_by_email(self, email: str) -> Optional[Customer]: ...
    def save(self, customer: Customer) -> None: ...
    def delete(self, id: str) -> None: ...

class OrderRepository(Protocol):
    def find_by_id(self, id: str) -> Optional[Order]: ...
    def find_by_customer_id(self, customer_id: str) -> List[Order]: ...
    def save(self, order: Order) -> None: ...
    def update(self, order: Order) -> None: ...
```

### Service Interfaces

External service interfaces:

```python
class NotificationService(Protocol):
    def send_email(self, to: str, subject: str, content: str) -> bool: ...
    def send_sms(self, to: str, message: str) -> bool: ...

class PaymentGateway(Protocol):
    def process_payment(self, order_id: str, amount: Money, payment_method: dict) -> bool: ...
    def refund_payment(self, payment_id: str, amount: Money) -> bool: ...
```

### Domain Events

Events that capture important occurrences in the domain:

```python
class DomainEvent:
    """Base class for all domain events"""
    def __init__(self):
        self.timestamp = datetime.now()
        self.id = str(uuid.uuid4())

class CustomerRegistered(DomainEvent):
    def __init__(self, customer_id: str):
        super().__init__()
        self.customer_id = customer_id

class OrderSubmitted(DomainEvent):
    def __init__(self, order_id: str, customer_id: str, total_amount: Money):
        super().__init__()
        self.order_id = order_id
        self.customer_id = customer_id
        self.total_amount = total_amount
```

### Domain Services

Services that encapsulate domain logic which doesn't naturally fit in a single entity:

```python
from enum import Enum
from decimal import Decimal
from typing import List

class PaymentMethod(Enum):
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    DIGITAL_WALLET = "digital_wallet"

class Payment:
    def __init__(self, method: PaymentMethod, amount: Decimal):
        self.method = method
        self.amount = amount
        self.card_number = None
        self.expiry_date = None
        self.cvv = None
        self.account_number = None
        self.routing_number = None

class PaymentDomainService:
    """Domain service for payment processing logic"""

    def calculate_transaction_fee(self, amount: Decimal, payment_method: PaymentMethod) -> Decimal:
        """Calculate transaction fee based on amount and payment method"""
        if payment_method == PaymentMethod.CREDIT_CARD:
            return max(Decimal('0.50'), amount * Decimal('0.029'))
        elif payment_method == PaymentMethod.BANK_TRANSFER:
            return Decimal('0')
        elif payment_method == PaymentMethod.DIGITAL_WALLET:
            return amount * Decimal('0.015')
        else:
            raise ValueError(f"Unsupported payment method: {payment_method}")

    def validate_payment_details(self, payment: Payment) -> List[str]:
        """Validate payment details based on payment method"""
        errors = []

        if payment.method == PaymentMethod.CREDIT_CARD:
            if not payment.card_number or len(payment.card_number) < 13:
                errors.append("Invalid card number")
            if not payment.expiry_date:
                errors.append("Expiry date required")
            if not payment.cvv or len(payment.cvv) < 3:
                errors.append("CVV required")

        elif payment.method == PaymentMethod.BANK_TRANSFER:
            if not payment.account_number:
                errors.append("Account number required")
            if not payment.routing_number:
                errors.append("Routing number required")

        return errors
```

## Guidelines for Clean Domain Design

1. **Focus on business rules** - The domain layer should reflect business requirements, not technical concerns

2. **Use ubiquitous language** - Domain code should use terminology that business stakeholders understand

3. **Protect invariants** - Ensure entities maintain valid state through proper validation and encapsulation

4. **Make implicit concepts explicit** - Identify hidden concepts and model them explicitly

5. **Design for behavior** - Model entities around their behavior, not just as data containers

6. **Isolate the domain** - Keep domain logic completely independent of infrastructure concerns

7. **Rich domain model** - Put business logic in the domain entities rather than in services when possible
