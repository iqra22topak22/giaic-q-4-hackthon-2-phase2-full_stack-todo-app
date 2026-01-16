<!--
Sync Impact Report:
- Version change: N/A (initial version) → 1.0.0
- Added sections: Core Principles (6), Additional Constraints, Development Workflow, Governance
- Templates requiring updates: N/A (initial creation)
- Follow-up TODOs: None
-->
# Todo Web Application Phase II Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
Spec-Kit Plus methodology is mandatory: Specifications are the single source of truth for all development. No implementation may begin without approved, complete specifications. All features must be defined with clear requirements, acceptance criteria, and testable scenarios before any code is written.

### II. Agentic Workflow (NON-NEGOTIABLE) 
All development work must be performed through defined agents and skills. No manual coding or ad-hoc decisions are allowed. The Qwen CLI with Spec-Kit Plus agents (auth-security-agent, backend-api-agent, frontend-todo-agent, orchestrator-agent, spec-analyst) must be used for all implementation tasks.

### III. Strict Phase Order (NON-NEGOTIABLE)
Development phases must be followed in strict sequence without skipping: sp.constitution → sp.specify → sp.plan → sp.tasks → sp.implement. Each phase must be completed and approved before proceeding to the next. Implementation is forbidden before sp.tasks approval.

### IV. Security-First Architecture
Security requirements take precedence over feature implementation. All authentication and authorization flows must be designed and validated before other functionality. JWT-based authentication with proper token validation and user-based data isolation are mandatory for all endpoints.

### V. Frontend-Backend Separation
Clear separation of concerns between frontend and backend: Frontend handles UI and user interactions only; Backend enforces all authorization and data validation. API contracts must be clearly defined and adhered to by both sides.

### VI. Test-First Development
All code must be developed with tests written first. Unit tests, integration tests, and end-to-end tests must be created as part of the development process. Code without adequate test coverage will not be accepted.

## Additional Constraints

### Technology Stack Requirements
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (Frontend) + JWT (Backend)
- Monorepo structure must be preserved throughout development

### Authentication & Security Requirements
- All API endpoints require a valid JWT token
- JWT tokens are issued by Better Auth on the frontend
- Backend must verify JWT signature and expiry using a shared secret
- user_id must be extracted from the JWT token only (never from request body, query params, or URL)
- All task operations must be filtered by the authenticated user's ID
- Requests without valid JWT must return 401 Unauthorized
- Cross-user data access is strictly forbidden

### API Behavior Standards
- RESTful API conventions must be followed
- All endpoints must be stateless
- Responses must only include data belonging to the authenticated user
- Proper HTTP status codes must be returned for all responses
- API responses must follow consistent structure

## Development Workflow

### Quality & Review Process
- If specs are missing, unclear, or conflicting, implementation must be blocked
- Security correctness has higher priority than feature completeness
- Agents are allowed to request spec updates before proceeding
- All code must pass through automated linting and type-checking
- Peer review is required before merging any changes

### Implementation Guidelines
- Frontend: JWT token must be attached to every API request via Authorization header
- Frontend: API calls must go through a centralized API client
- Backend: SQLModel must be used for all database interactions
- Backend: Environment variables must be used for secrets and configuration
- No direct fetch in frontend components; all API calls must go through centralized client

## Governance

This constitution supersedes all other development practices for Phase II of the Todo Web Application. All development activities must verify compliance with these principles. Any complexity must be justified against these principles. All pull requests and code reviews must verify constitutional compliance. This constitution is immutable for the remainder of Phase II and any amendments require explicit documentation, approval, and migration planning.

**Version**: 1.0.0 | **Ratified**: 2026-01-07 | **Last Amended**: 2026-01-07