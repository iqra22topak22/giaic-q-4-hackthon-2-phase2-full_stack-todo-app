# Data Model: Frontend Todo UI with Authentication

## Entities

### User Session
- **Fields**: 
  - userId: string (from JWT payload)
  - token: string (JWT token)
  - expiresAt: Date (token expiration)
  - isAuthenticated: boolean
- **Relationships**: Contains JWT token used for API authentication
- **Validation**: Token must be valid JWT, not expired
- **State Transitions**: Unauthenticated → Authenticating → Authenticated → SignedOut

### Task
- **Fields**:
  - id: string (unique identifier from backend)
  - title: string (required, max 255 chars)
  - description?: string (optional, max 1000 chars)
  - status: 'pending' | 'completed' (default: 'pending')
  - createdAt: Date (set by backend)
  - updatedAt: Date (set by backend)
  - userId: string (from JWT, validated by backend)
- **Relationships**: Belongs to a user (via userId)
- **Validation**: Title is required, status must be valid enum value
- **State Transitions**: pending → completed, completed → pending

### Authentication Form
- **Fields**:
  - email: string (valid email format)
  - password: string (min 8 chars, with complexity)
  - confirmPassword?: string (for signup only)
- **Relationships**: Used to authenticate user and obtain session
- **Validation**: Email format, password complexity, matching passwords on signup
- **State Transitions**: Form filled → Validated → Submitted → Result received

### Task Form
- **Fields**:
  - title: string (required, max 255 chars)
  - description?: string (optional, max 1000 chars)
  - status: 'pending' | 'completed' (default: 'pending')
- **Relationships**: Used to create or update Task entities
- **Validation**: Title is required
- **State Transitions**: Form initialized → Filled → Validated → Submitted → Result received