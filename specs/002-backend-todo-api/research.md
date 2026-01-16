# Research Summary: Backend API for Todo Web Application

**Feature**: 002-backend-todo-api
**Date**: 2026-01-08

## Overview

This document summarizes the research conducted to support the implementation of the backend API for the Todo Web Application. It addresses all technical decisions and clarifications needed for the project.

## Technology Stack Research

### Python & FastAPI
- **Decision**: Use Python 3.11 with FastAPI framework
- **Rationale**: FastAPI offers automatic API documentation, type validation, and high performance. It's ideal for building APIs with built-in validation and serialization.
- **Alternatives considered**: Flask, Django REST Framework
- **Justification**: FastAPI's automatic OpenAPI generation and Pydantic integration provide superior developer experience and API documentation.

### Database & ORM
- **Decision**: Use SQLModel as the ORM with Neon Serverless PostgreSQL
- **Rationale**: SQLModel combines SQLAlchemy and Pydantic, allowing shared models between request validation and database operations. Neon Serverless provides serverless PostgreSQL with excellent scaling.
- **Alternatives considered**: Pure SQLAlchemy, Tortoise ORM, Peewee
- **Justification**: SQLModel's compatibility with both Pydantic and SQLAlchemy makes it ideal for FastAPI applications.

### Authentication
- **Decision**: Implement JWT-based authentication using PyJWT
- **Rationale**: JWT tokens are stateless and can be verified without server-side storage. Better Auth generates JWTs that can be validated with a shared secret.
- **Alternatives considered**: Session-based authentication, OAuth2 with password flow
- **Justification**: JWT aligns with the frontend's Better Auth implementation and provides stateless authentication.

## Architecture Patterns

### Project Structure
- **Decision**: Use modular structure with separate directories for models, schemas, API routes, and utilities
- **Rationale**: Modular structure improves maintainability and makes the codebase easier to navigate
- **Alternatives considered**: Single-file application, flat directory structure
- **Justification**: Modular approach scales better as the application grows

### Dependency Injection
- **Decision**: Use FastAPI's built-in dependency injection system
- **Rationale**: FastAPI's dependency injection provides automatic validation, shared dependencies, and clean code organization
- **Alternatives considered**: Manual dependency passing, third-party DI libraries
- **Justification**: Built-in system integrates seamlessly with FastAPI's validation and documentation features

### Database Session Management
- **Decision**: Use dependency injection to provide database sessions to route handlers
- **Rationale**: Ensures proper session cleanup and reduces boilerplate code in route handlers
- **Alternatives considered**: Global session objects, manual session creation in each handler
- **Justification**: Dependency injection ensures sessions are properly closed and follows FastAPI best practices

## Security Considerations

### JWT Validation
- **Decision**: Validate JWT tokens using the shared secret from Better Auth
- **Rationale**: Ensures tokens were issued by the legitimate authentication system
- **Implementation details**: Extract token from Authorization header, decode using PyJWT with shared secret, verify expiration
- **Security measures**: Check token expiration, verify signature, validate issuer if present

### User Isolation
- **Decision**: Filter all queries by the authenticated user's ID extracted from JWT
- **Rationale**: Prevents users from accessing other users' data
- **Implementation details**: Extract user_id from JWT in authentication dependency, pass to route handlers, use in all database queries
- **Security measures**: Never trust user_id from request body or URL, always use the one from the token

## API Design

### Endpoint Structure
- **Decision**: Use RESTful endpoints with user_id in the path
- **Rationale**: Clear ownership semantics and easy to understand URL structure
- **Pattern**: `/api/{user_id}/tasks`, `/api/{user_id}/tasks/{id}`
- **Alternatives considered**: Endpoints without user_id (relying on token only)
- **Justification**: Including user_id in the path makes ownership explicit and aligns with REST principles

### Error Handling
- **Decision**: Use consistent error response format with appropriate HTTP status codes
- **Rationale**: Provides predictable error handling for frontend developers
- **Implementation details**: Custom exception handlers, consistent error response schema
- **Status codes**: 401 for auth errors, 403 for authorization errors, 404 for not found, 422 for validation errors

## Performance Considerations

### Database Queries
- **Decision**: Use async database operations with SQLModel
- **Rationale**: Prevents blocking the event loop and improves concurrency
- **Implementation details**: Use async/await with SQLModel and asyncpg driver
- **Performance benefits**: Higher throughput under concurrent load

### Connection Pooling
- **Decision**: Configure appropriate connection pool settings for Neon Serverless
- **Rationale**: Optimizes database connection reuse and reduces overhead
- **Settings**: Min and max pool sizes appropriate for expected load
- **Considerations**: Neon's serverless nature affects connection lifecycle

## Testing Strategy

### Test Types
- **Decision**: Implement unit, integration, and contract tests
- **Rationale**: Comprehensive testing ensures reliability and catches issues early
- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test API endpoints with mocked or real database
- **Contract tests**: Verify API contracts match specifications

### Test Framework
- **Decision**: Use pytest with FastAPI test client
- **Rationale**: pytest provides powerful testing features and integrates well with FastAPI
- **Features**: Fixtures, parametrized tests, clear reporting
- **Integration**: FastAPI's test client simulates HTTP requests without running a server

## Deployment Considerations

### Environment Variables
- **Decision**: Store sensitive configuration in environment variables
- **Rationale**: Keeps secrets out of code and allows different configs per environment
- **Variables**: Database URL, JWT secret, API keys
- **Management**: Different approaches for local development vs cloud deployment

### CORS Configuration
- **Decision**: Configure CORS to allow requests from frontend domains
- **Rationale**: Enables frontend to make API requests while maintaining security
- **Settings**: Allow credentials, specific origins, appropriate methods and headers
- **Security**: Restrict origins in production, avoid wildcard in production

## Future Extensibility

### API Versioning
- **Decision**: Implement versioning in the URL path (e.g., /api/v1/)
- **Rationale**: Allows backward-compatible changes and clear API evolution
- **Implementation**: Organize routes under versioned paths
- **Benefits**: Easy to maintain multiple API versions, clear migration path

### Monitoring & Observability
- **Decision**: Plan for logging, metrics, and tracing
- **Rationale**: Essential for production monitoring and debugging
- **Components**: Structured logging, performance metrics, request tracing
- **Tools**: Integrate with standard observability platforms