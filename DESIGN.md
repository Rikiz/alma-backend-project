# FastAPI Leads Service Design Document

## Overview

This design document details the architectural design and technology selection decisions for the FastAPI Leads Service. The system is a modern lead (potential customer) management system that adopts an asynchronous architecture design, supporting resume file uploads, email notifications, and status tracking.

## Architectural Design Principles

### 1. Async-First Architecture

**Design Decision**: Adopt FastAPI + asyncio asynchronous architecture

**Reasons**:
- **High Concurrency Handling**: Asynchronous architecture better handles high-concurrency requests, especially I/O-intensive operations like file uploads and email sending
- **Resource Efficiency**: Asynchronous programming can significantly reduce thread switching overhead and improve CPU utilization
- **Modern Web Standards**: FastAPI is based on Starlette and supports ASGI standards, providing better asynchronous performance
- **Mature Ecosystem**: The Python asynchronous ecosystem is mature, with libraries like aiofiles and aiosmtplib providing complete asynchronous support

**Implementation Details**:
- Use `aiofiles` for asynchronous file I/O operations
- Use `aiosmtplib` for asynchronous email sending
- The API layer is fully asynchronous, supporting concurrent processing of multiple requests

### 2. Modular Layered Architecture

**Design Decision**: Adopt a clear layered architecture design

```
app/
├── api/           # API routing layer
├── core/          # Core configuration
├── models/        # Data models
├── services/      # Business service layer
├── server/        # Data access layer
└── database/      # Database configuration
```

**Reasons**:
- **Separation of Concerns**: Each layer has clear responsibilities, facilitating maintenance and testing
- **Scalability**: New features can be easily added to the corresponding layer
- **Code Reusability**: Service layer can be reused by multiple API endpoints

**Responsibilities of Each Layer**:
- **API Layer**: Handles HTTP requests/responses and route definitions
- **Service Layer**: Business logic, file processing, email sending
- **Data Access Layer**: Database CRUD operations
- **Model Layer**: Data structure definitions and validation

## Technology Stack Selection

### 3. Web Framework: FastAPI

**Reasons for Selection**:
- **Automatic API Documentation**: Generates interactive documentation based on OpenAPI standards
- **Type Safety**: Request/response validation based on Pydantic
- **Async-Native**: Fully supports asynchronous programming
- **Excellent Performance**: Based on Starlette, performance close to native ASGI
- **Development Experience**: Hot reloading, dependency injection, built-in test client

### 4. ORM: SQLAlchemy 2.0

**Reasons for Selection**:
- **Mature and Stable**: Python's most popular ORM framework
- **Flexibility**: Supports multiple database backends (SQLite/PostgreSQL)
- **Async Support**: Version 2.0 natively supports asynchronous operations
- **Expressive Queries**: Powerful query construction API
- **Migration Support**: Integrates with Alembic for database migrations

### 5. Data Validation: Pydantic V2

**Reasons for Selection**:
- **Type Safety**: Runtime type checking and conversion
- **Serialization**: Automatic JSON serialization/deserialization
- **Validation Rules**: Rich built-in validators and custom validation
- **FastAPI Integration**: Native integration for seamless collaboration

### 6. Async File Processing: aiofiles

**Reasons for Selection**:
- **Async I/O**: Non-blocking file operations
- **Compatibility**: Compatible with standard `open()` API
- **Memory Efficiency**: Supports chunked processing for large files
- **Ecosystem Integration**: Perfect integration with FastAPI's `UploadFile`

### 7. Async Email: aiosmtplib

**Reasons for Selection**:
- **Async Sending**: Non-blocking email sending
- **Protocol Support**: Supports SMTP/TLS/SSL
- **Error Handling**: Comprehensive exception handling mechanisms
- **Configuration Flexibility**: Supports multiple email service providers

### 8. Configuration Management: Pydantic Settings

**Reasons for Selection**:
- **Environment Variables**: Automatically reads environment variables
- **Type Safety**: Type checking for configuration items
- **Validation**: Configuration value validation and conversion
- **Documentation**: Automatic documentation of configuration items

## Data Model Design

### 9. Lead Data Model

**Design Decision**: Streamlined core field design

```python
class Lead(Base):
    id: Primary Key
    first_name: str (128)
    last_name: str (128)
    email: str (256, indexed)
    resume_path: str (512, optional)
    state: Enum (PENDING/REACHED_OUT)
    created_at: datetime
    updated_at: datetime
```

**Design Considerations**:
- **Required Fields**: Core business information must be provided
- **Field Length Limits**: Prevents database storage overflow
- **Email Uniqueness**: Ensures business uniqueness through indexing
- **Timestamps**: Automatically maintains creation and update times

### 10. Status Enum Design

**Reasons for Selection**:
- **Business Semantics**: PENDING (pending), REACHED_OUT (contacted)
- **Extensibility**: Enums are easy to extend with new statuses
- **Type Safety**: Prevents invalid status values
- **Database Friendly**: Stored as strings for readability

## API Design Patterns

### 11. RESTful API Design

**Public APIs**:
- `POST /public/create_leads`: Create new lead
- `PUT /public/update_leads/{id}`: Update existing lead

**Internal APIs**:
- `GET /internal/leads`: Get all leads
- `GET /internal/leads/{id}`: Get single lead
- `PATCH /internal/leads/{id}/state`: Update status
- `DELETE /internal/leads/{id}`: Delete lead

**Design Decisions**:
- **Permission Separation**: Public APIs for customers, internal APIs for administrators
- **Operation Granularity**: Fine-grained CRUD operations
- **REST Principles**: Uses HTTP method semantics
- **Path Design**: Clear resource hierarchy

### 12. File Upload Processing

**Design Decision**: Multipart Form-Data + Asynchronous Processing

**Implementation Features**:
- **Streaming Processing**: Chunked reading of large files, memory-friendly
- **File Name Security**: UUID generation for unique file names
- **Extension Preservation**: Maintains original file extensions
- **Directory Management**: Automatic creation of upload directories

### 13. Form Data Validation

**Custom Form Support**:
```python
@as_form
class LeadForm(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: str = Field(..., min_length=1, max_length=128)
    email: EmailStr
```

**Design Rationale**:
- **FastAPI Compatibility**: Extends Pydantic support for Form data
- **Ease of Modification**: Based on Pydantic, allows modification of corresponding field validation rules

## Service Layer Design

### 14. Business Service Separation

**Storage Service (storage_service.py)**:
- File save and delete operations
- Path management and security checks

**Email Service (email_service.py)**:
- Email template and sending logic
- Configuration validation and error handling

**Design Decisions**:
- **Single Responsibility**: Each service focuses on one business domain
- **Reusability**: Services can be called by multiple API endpoints
- **Error Isolation**: Service-level errors do not affect other functions

### 15. Email Notification Architecture

**Asynchronous Processing**:
- Use `asyncio.create_task()` to create background tasks
- Non-blocking email sending that doesn't affect API response times
- Comprehensive error handling and logging

## Database Design

### 16. SQLite as Default Database

**Reasons for Selection**:
- **Zero Configuration**: No additional installation or configuration required
- **File Database**: Suitable for small applications and development environments
- **ACID Transactions**: Complete database transaction support
- **SQLAlchemy Compatibility**: Fully supports all features
- **Migration Convenience**: Easy switching to PostgreSQL

### 17. Data Access Layer (DAO) Pattern

**Design Decision**: Independent DAO layer encapsulates database operations

**Advantages**:
- **Data Access Abstraction**: API layer doesn't need to know database details
- **Transaction Management**: Each operation manages database sessions independently
- **Performance Optimization**: Unified addition of caching, connection pools, etc.

## Configuration and Deployment

### 18. Environment Variable Configuration

**Design Decision**: Configuration management based on Pydantic Settings

**Configuration Categories**:
- **Required Configuration**: DATABASE_URL, UPLOAD_DIR
- **Optional Configuration**: SMTP settings (email functionality)
- **Default Values**: Reasonable development environment defaults

**Advantages**:
- **Environment Isolation**: Different environments use different configurations
- **Security**: Sensitive information managed through environment variables
- **Validation**: Automatic validation and type conversion of configuration values

## Error Handling and Exception Management

### 19. Layered Exception Handling

**Custom Exception Classes**:
```python
class EmailError(Exception): ...
class EmailConfigurationError(EmailError): ...
class EmailSendError(EmailError): ...
```

**Exception Handling Strategies**:
- **API Layer**: HTTP exceptions converted to appropriate status codes
- **Service Layer**: Detailed error information for business exceptions
- **Global Handling**: Unified handling of uncaught exceptions

### 20. Email Sending Fault Tolerance

**Design Decision**: Email failures do not affect core business processes

**Fault Tolerance Mechanisms**:
- Email sending executes asynchronously in the background
- Sending failures only log errors, do not affect lead creation
- Comprehensive error classification and handling

## Performance Optimization Considerations

### 22. Asynchronous Architecture Optimization

**Performance Advantages**:
- **Concurrent Processing**: Simultaneous processing of multiple file uploads and email sending
- **Resource Utilization**: Reduces thread switching and memory usage
- **Response Time**: Non-blocking I/O operations improve response speed

### 23. Database Optimization

**Indexing Strategy**:
- email field index: Supports email duplication checks
- created_at descending order: Optimizes list query performance

**Query Optimization**:
- Paginated queries: Avoid loading large amounts of data at once
- Selective fields: Query only needed fields

## Extensibility and Maintainability

### 24. Modular Design

**Extension Points**:
- **New Services**: Easily add new business services
- **New APIs**: Add new endpoints following existing patterns
- **New States**: Enum extension supports new business states

## Deployment and Operations

### 25. Containerization Support

**Docker Deployment**:
```dockerfile
FROM python:3.11-slim
# Lightweight base image
# Complete dependency packaging
# Environment variable configuration
```

### 26. Production Environment Considerations

**WSGI Server**: Gunicorn + Uvicorn Workers
**Process Management**: Multiple worker processes for increased concurrency
**Logging Configuration**: Structured logging for monitoring
**Monitoring Endpoints**: Health checks and metrics exposure

## Summary

This FastAPI Leads Service design embodies modern web application best practices:

- **Async-First**: Fully leverages the advantages of Python asynchronous programming
- **Layered Architecture**: Clear separation of concerns and modular design
- **Type Safety**: End-to-end type checking and validation
- **Extensibility**: Easy addition of new features and extension of existing functionality
- **Production-Ready**: Comprehensive error handling, configuration management, and deployment support

Through careful selection of technology stacks and architectural patterns, the system not only meets current requirements but also lays a solid foundation for future expansion and maintenance.
