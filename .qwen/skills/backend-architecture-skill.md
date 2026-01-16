# Backend Architecture Skill

**Purpose**: Ensure clean, secure, and scalable backend design.

## Stack
- FastAPI
- SQLModel
- Neon PostgreSQL

## Actions
- Design RESTful endpoints
- Enforce user-based data isolation
- Apply ORM best practices
- Structure routes, models, and services correctly

## Rules
- All requests must be authenticated
- user_id must come from JWT, not request input

## RESTful Endpoint Design

### HTTP Method Usage
- [ ] GET: Retrieve resources (idempotent, safe)
- [ ] POST: Create new resources
- [ ] PUT: Update entire resources
- [ ] PATCH: Partial resource updates
- [ ] DELETE: Remove resources

### Endpoint Structure
- [ ] Use plural nouns for resource names (e.g., /users, /tasks)
- [ ] Use nested routes for relationships (e.g., /users/{user_id}/tasks)
- [ ] Use consistent naming conventions
- [ ] Follow standard HTTP status codes
- [ ] Implement proper pagination for list endpoints
- [ ] Use query parameters for filtering and sorting

### Response Format
- [ ] Consistent response structure
- [ ] Proper error response format
- [ ] Include relevant metadata (pagination, counts)
- [ ] Use appropriate HTTP status codes
- [ ] Include HATEOAS links where appropriate

## Authentication and Authorization

### JWT Implementation
- [ ] All endpoints require authentication unless explicitly public
- [ ] JWT tokens validated using proper middleware
- [ ] Token expiration handled properly
- [ ] Refresh token mechanism implemented
- [ ] Secure token storage and transmission

### User-Based Data Isolation
- [ ] Every request extracts user_id from JWT token (never from request body/params)
- [ ] All database queries filter by user_id for data isolation
- [ ] Access control checks before data operations
- [ ] Proper validation of resource ownership
- [ ] Error responses that don't leak information about other users' data

## ORM Best Practices with SQLModel

### Model Design
- [ ] Use SQLModel for all database models
- [ ] Define proper relationships between models
- [ ] Use appropriate field types and constraints
- [ ] Implement proper indexing strategies
- [ ] Use enums for fields with limited options
- [ ] Define proper foreign key relationships

### Query Optimization
- [ ] Use select statements with specific fields when possible
- [ ] Implement proper pagination for large datasets
- [ ] Use joins efficiently to minimize queries
- [ ] Implement proper caching strategies
- [ ] Use transactions for multi-step operations
- [ ] Avoid N+1 query problems

### Migration Strategy
- [ ] Use Alembic for database migrations
- [ ] Version control for schema changes
- [ ] Proper rollback capabilities
- [ ] Test migrations in development first
- [ ] Backup strategy before migrations

## Service Layer Architecture

### Business Logic Separation
- [ ] Keep business logic in service layer, not in route handlers
- [ ] Create dedicated service classes/functions for complex operations
- [ ] Implement proper input validation in services
- [ ] Separate concerns between data access and business logic
- [ ] Use dependency injection where appropriate

### Error Handling
- [ ] Centralized error handling
- [ ] Custom exception classes for domain-specific errors
- [ ] Proper logging of errors
- [ ] User-friendly error messages
- [ ] Avoid exposing internal system details

## Security Measures

### Input Validation
- [ ] Validate all input parameters
- [ ] Sanitize user inputs to prevent injection attacks
- [ ] Implement rate limiting for endpoints
- [ ] Use proper encoding for special characters
- [ ] Validate file uploads if applicable

### Data Protection
- [ ] Encrypt sensitive data at rest
- [ ] Use HTTPS for all communications
- [ ] Implement proper CORS policies
- [ ] Sanitize data before returning to clients
- [ ] Protect against common vulnerabilities (XSS, CSRF, etc.)

## Route Organization

### Route Structure
- [ ] Organize routes by domain/feature
- [ ] Use consistent URL patterns
- [ ] Implement proper middleware for authentication
- [ ] Group related endpoints in routers
- [ ] Use prefix for API versioning if needed

### Middleware Implementation
- [ ] Authentication middleware for protected routes
- [ ] Logging middleware for request/response tracking
- [ ] Rate limiting middleware
- [ ] Request validation middleware
- [ ] Error handling middleware

## Database Design with Neon PostgreSQL

### Connection Management
- [ ] Use connection pooling
- [ ] Proper session management
- [ ] Handle connection timeouts gracefully
- [ ] Implement retry logic for failed connections
- [ ] Monitor connection usage

### Schema Design
- [ ] Normalize database schema appropriately
- [ ] Use proper indexing strategies
- [ ] Implement proper constraints
- [ ] Design for scalability from the start
- [ ] Plan for data archiving/retention

## Testing Strategy

### Test Coverage
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Database integration tests
- [ ] Authentication and authorization tests
- [ ] Performance tests for critical endpoints

### Test Organization
- [ ] Separate test files by feature/domain
- [ ] Use fixtures for test data
- [ ] Mock external dependencies
- [ ] Test both positive and negative scenarios
- [ ] Include security-focused tests

## Monitoring and Observability

### Logging
- [ ] Structured logging with appropriate levels
- [ ] Log important business events
- [ ] Include request IDs for traceability
- [ ] Avoid logging sensitive information
- [ ] Implement log rotation

### Metrics
- [ ] Track API response times
- [ ] Monitor error rates
- [ ] Track database query performance
- [ ] Monitor resource usage
- [ ] Set up alerts for anomalies

## Quality Checks

### Before Endpoint Creation:
- [ ] Verify authentication requirements
- [ ] Confirm user_id extraction from JWT
- [ ] Plan data isolation strategy
- [ ] Design proper response format

### Before Database Operations:
- [ ] Ensure user_id filter is applied where needed
- [ ] Verify proper relationships are defined
- [ ] Check for potential N+1 queries
- [ ] Confirm transaction boundaries

### Before Deployment:
- [ ] Run all tests successfully
- [ ] Verify security measures are in place
- [ ] Check performance under load
- [ ] Validate error handling
- [ ] Confirm data isolation works properly