# Frontend Architecture Skill

**Purpose**: Guide correct frontend architectural decisions.

## Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth

## Actions
- Decide server vs client components
- Enforce centralized API client usage
- Ensure JWT token attachment to requests
- Maintain responsive and accessible UI structure

## Rules
- No backend logic
- No direct fetch inside components

## Component Architecture Guidelines

### Server Components vs Client Components

#### Use Server Components When:
- [ ] Initial data fetching that doesn't change frequently
- [ ] Rendering data that doesn't require client-side interactivity
- [ ] Server-side authentication checks
- [ ] SEO-sensitive content rendering
- [ ] Initial page load optimization
- [ ] Accessing server-side environment variables

#### Use Client Components When:
- [ ] Handling user interactions (clicks, form submissions)
- [ ] Managing client-side state
- [ ] Using browser APIs (localStorage, geolocation, etc.)
- [ ] Implementing animations or dynamic UI changes
- [ ] Working with third-party libraries that require browser APIs
- [ ] Real-time updates (websockets, etc.)

### API Client Architecture

#### Centralized API Client Requirements:
- [ ] Single API client instance for the entire application
- [ ] Interceptors for JWT token attachment
- [ ] Consistent error handling
- [ ] Request/response type definitions
- [ ] Retry mechanisms for failed requests
- [ ] Timeout configurations

#### API Client Implementation:
- [ ] Create API client in a dedicated file (e.g., lib/api-client.ts)
- [ ] Implement axios or fetch wrapper with interceptors
- [ ] Add JWT token to Authorization header automatically
- [ ] Handle token refresh when expired
- [ ] Implement proper error response handling

## Authentication Architecture

### Better Auth Integration:
- [ ] Initialize Better Auth at the application root
- [ ] Create authentication context/provider
- [ ] Implement token storage and retrieval
- [ ] Handle authentication state across components
- [ ] Implement protected route components
- [ ] Create authentication hooks

### JWT Token Management:
- [ ] Securely store JWT tokens (preferably in httpOnly cookies)
- [ ] Implement token refresh mechanisms
- [ ] Handle token expiration gracefully
- [ ] Attach tokens to all authenticated API requests
- [ ] Implement logout functionality

## UI Architecture Principles

### Responsive Design:
- [ ] Mobile-first approach with Tailwind CSS
- [ ] Breakpoints defined using Tailwind's standard sizes
- [ ] Flexible layouts using grid and flexbox
- [ ] Properly sized touch targets
- [ ] Readable typography across devices

### Accessibility:
- [ ] Semantic HTML structure
- [ ] Proper ARIA attributes
- [ ] Keyboard navigation support
- [ ] Sufficient color contrast
- [ ] Screen reader compatibility
- [ ] Focus management

## Anti-Patterns to Avoid

### Backend Logic in Frontend:
- [ ] No direct database queries
- [ ] No business logic implementation
- [ ] No server-side validation in frontend
- [ ] No file system operations
- [ ] No environment variable access that should be server-only

### Direct Fetch in Components:
- [ ] No `fetch` calls directly in components
- [ ] No `axios.get` directly in component functions
- [ ] No API calls without going through centralized client
- [ ] No hardcoded API endpoints in components
- [ ] No manual token management in components

## File Structure Recommendations

### Recommended Structure:
```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication-related pages
│   ├── (protected)/       # Protected routes
│   └── api/               # API routes (if needed)
├── components/            # Reusable UI components
│   ├── ui/                # Base UI components
│   └── modules/           # Feature-specific components
├── lib/                   # Utilities and API client
│   ├── api-client.ts      # Centralized API client
│   ├── auth.ts            # Authentication utilities
│   └── types.ts           # TypeScript type definitions
├── hooks/                 # Custom React hooks
├── contexts/              # React context providers
└── styles/                # Global styles
```

## Type Safety Requirements

### TypeScript Implementation:
- [ ] Strict mode enabled in tsconfig.json
- [ ] Type definitions for all API responses
- [ ] Type definitions for component props
- [ ] Type definitions for state objects
- [ ] Type definitions for API request parameters
- [ ] Proper error type handling

## Quality Checks

### Before Component Creation:
- [ ] Determine if server or client component is needed
- [ ] Verify no direct API calls are planned
- [ ] Confirm component fits in the architecture
- [ ] Check if existing component can be reused

### Before API Integration:
- [ ] Verify using centralized API client
- [ ] Confirm JWT token will be attached automatically
- [ ] Check proper error handling implementation
- [ ] Validate request/response typing

### Before Authentication Implementation:
- [ ] Confirm using Better Auth patterns
- [ ] Verify token handling through proper channels
- [ ] Check protected route implementation
- [ ] Validate logout functionality