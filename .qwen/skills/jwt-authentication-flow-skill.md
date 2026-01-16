# JWT Authentication Flow Skill

**Purpose**: Guarantee secure authentication and authorization across the stack.

## Actions
- Define Better Auth → JWT issuance
- Ensure frontend sends JWT correctly
- Ensure backend verifies JWT signature and expiry
- Enforce task ownership via decoded user_id

## Security Rules
- Shared secret via environment variable
- Reject missing or invalid tokens (401)
- Prevent cross-user data access

## Authority
- Can block implementation if JWT flow is insecure

## JWT Token Lifecycle

### 1. Token Issuance (Better Auth)
- [ ] JWT contains user_id in the payload
- [ ] Token includes proper expiration time (exp claim)
- [ ] Token includes issued-at time (iat claim)
- [ ] Token is signed with secure algorithm (HS256/RS256)
- [ ] Shared secret is stored in environment variable
- [ ] Token includes appropriate claims for authorization

### 2. Token Storage (Frontend)
- [ ] Secure storage of JWT (preferably httpOnly cookies)
- [ ] Proper token refresh mechanism
- [ ] Secure transmission (HTTPS only)
- [ ] Token expiration handling
- [ ] Secure logout functionality

### 3. Token Transmission (Frontend → Backend)
- [ ] JWT attached to Authorization header: "Bearer {token}"
- [ ] Token sent with every authenticated request
- [ ] Proper error handling for token-related failures
- [ ] Automatic token refresh when needed
- [ ] No tokens in URL parameters or request body

### 4. Token Verification (Backend)
- [ ] Validate JWT signature using shared secret
- [ ] Check token expiration (exp claim)
- [ ] Verify token structure and format
- [ ] Extract user_id from token payload
- [ ] Validate token hasn't been tampered with

## Frontend Implementation Requirements

### Better Auth Integration
- [ ] Initialize Better Auth with proper configuration
- [ ] Implement login and registration flows
- [ ] Handle authentication state properly
- [ ] Implement protected route components
- [ ] Create authentication context/provider

### API Client Configuration
- [ ] Configure centralized API client with JWT interceptor
- [ ] Automatically attach JWT to Authorization header
- [ ] Handle token refresh automatically
- [ ] Implement proper error handling for 401 responses
- [ ] Retry requests after token refresh if needed

### Token Management
- [ ] Secure token storage (avoid localStorage for sensitive tokens)
- [ ] Implement token refresh before expiration
- [ ] Handle token invalidation/logout properly
- [ ] Secure token transmission (HTTPS only)
- [ ] Implement proper error states for auth failures

## Backend Implementation Requirements

### Authentication Middleware
- [ ] Create middleware to verify JWT tokens
- [ ] Extract user_id from token payload
- [ ] Return 401 for invalid/missing tokens
- [ ] Pass user_id to request context
- [ ] Handle token expiration properly

### Route Protection
- [ ] Apply authentication middleware to protected routes
- [ ] Verify token exists and is valid for each request
- [ ] Extract user_id from JWT (never from request body/params)
- [ ] Implement proper error responses for auth failures
- [ ] Log authentication-related events

### Data Isolation
- [ ] Filter database queries by user_id from JWT
- [ ] Verify resource ownership before operations
- [ ] Prevent cross-user data access
- [ ] Implement proper authorization checks
- [ ] Return consistent error messages

## Security Validation Checklist

### 1. Token Security
- [ ] Shared secret stored in environment variable (not hardcoded)
- [ ] JWT uses secure signing algorithm
- [ ] Proper token expiration times
- [ ] No sensitive information in token payload
- [ ] Secure token transmission (HTTPS)

### 2. Implementation Security
- [ ] All endpoints properly protected
- [ ] user_id always comes from JWT, never request input
- [ ] No direct fetch in frontend components
- [ ] Centralized API client used consistently
- [ ] Proper error handling without information leakage

### 3. Data Isolation
- [ ] Database queries filtered by user_id
- [ ] Resource ownership verified before operations
- [ ] Cross-user access prevented
- [ ] Proper authorization checks in place
- [ ] Consistent error responses

## Error Handling

### 401 Unauthorized Scenarios
- [ ] Missing Authorization header
- [ ] Invalid JWT format
- [ ] Expired token
- [ ] Invalid signature
- [ ] Revoked token

### Error Response Format
- [ ] Consistent error response structure
- [ ] Appropriate HTTP status code (401)
- [ ] User-friendly error message
- [ ] No sensitive information leakage
- [ ] Proper logging of security events

## Quality Gates

### Before Implementation
- [ ] JWT configuration properly defined
- [ ] Shared secret stored securely
- [ ] Authentication flow designed
- [ ] Token refresh mechanism planned
- [ ] Data isolation strategy defined

### During Implementation
- [ ] All endpoints require authentication
- [ ] user_id extracted from JWT correctly
- [ ] Database queries filter by user_id
- [ ] Frontend sends JWT in Authorization header
- [ ] Backend verifies JWT properly

### Before Approval
- [ ] Security validation checklist completed
- [ ] Penetration testing performed if applicable
- [ ] Code review completed by security expert
- [ ] All security rules implemented
- [ ] Authority to block if insecure flow detected

## Blocking Criteria

This skill has authority to block implementation if:
- [ ] JWT tokens are not properly validated
- [ ] user_id is taken from request instead of JWT
- [ ] Shared secret is hardcoded in code
- [ ] Cross-user data access is possible
- [ ] Authentication can be bypassed
- [ ] Tokens are transmitted insecurely
- [ ] Missing or inadequate error handling
- [ ] Any other critical security vulnerability