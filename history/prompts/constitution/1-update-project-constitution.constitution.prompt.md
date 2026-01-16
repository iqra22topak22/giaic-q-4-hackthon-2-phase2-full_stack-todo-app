---
id: 1
title: Update project constitution
stage: constitution
date: 2026-01-07
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - phase-2
  - todo-app
links:
  - spec: null
  - ticket: null
  - adr: null
  - pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
  - .specify/templates/tasks-template.md
tests: []
---

# Update project constitution

## Prompt Text

/sp.constitution You are initiating sp.constitution for Phase II of the Todo Full-Stack Web Application.

CONTEXT:
- Phase I (console app) is already completed.
- Phase II goal is to transform the console app into a secure, multi-user, full-stack web application.
- This project uses Spec-Kit Plus methodology and is executed via Qwen CLI.
- Agents and skills are already defined under .qwen/agents and .qwen/skills.

OBJECTIVE OF THIS CONSTITUTION:
Define immutable rules, constraints, and development principles that MUST be followed for Phase II.

CORE PRINCIPLES:
1. Spec-Driven Development is mandatory.
   - Specs are the single source of truth.
   - No implementation may begin without approved specs.

2. Agentic Workflow is mandatory.
   - All work must be performed through defined agents.
   - Skills must be used where applicable.
   - No manual coding or ad-hoc decisions are allowed.

3. Phase Order is strict and cannot be skipped:
   - sp.constitution
   - sp.specify
   - sp.plan
   - sp.tasks
   - sp.implement

TECHNOLOGY CONSTRAINTS:
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (Frontend) + JWT
- Monorepo structure must be preserved.

AUTHENTICATION & SECURITY RULES:
- All API endpoints require a valid JWT token.
- JWT tokens are issued by Better Auth on the frontend.
- Backend must verify JWT signature and expiry using a shared secret.
- user_id must be extracted from the JWT token only.
- Backend must NEVER trust user_id from request body, query params, or URL.
- All task operations must be filtered by the authenticated user's ID.
- Requests without valid JWT must return 401 Unauthorized.

API BEHAVIOR RULES:
- RESTful API conventions must be followed.
- All endpoints must be stateless.
- Responses must only include data belonging to the authenticated user.
- Cross-user data access is strictly forbidden.

FRONTEND RULES:
- Frontend handles authentication and UI only.
- JWT token must be attached to every API request via Authorization header.
- API calls must go through a centralized API client.
- No direct backend logic or data validation beyond UI concerns.

BACKEND RULES:
- Backend enforces all authorization and data isolation.
- SQLModel must be used for all database interactions.
- Environment variables must be used for secrets and configuration.

QUALITY & REVIEW RULES:
- If specs are missing, unclear, or conflicting, implementation must be blocked.
- Security correctness has higher priority than feature completeness.
- Agents are allowed to request spec updates before proceeding.

OUTPUT EXPECTATION:
- Produce a clear and final Phase II constitution.
- This constitution is immutable for the remainder of Phase II.
- All subsequent phases must comply with this constitution.

## Response Text

I have successfully updated the project constitution for Phase II of the Todo Full-Stack Web Application. Here's what I did:

1. Created a comprehensive constitution file at `.specify/memory/constitution.md` that includes:
   - Six core principles including Spec-Driven Development, Agentic Workflow, Strict Phase Order, Security-First Architecture, Frontend-Backend Separation, and Test-First Development
   - Additional constraints for technology stack and authentication/security requirements
   - Development workflow guidelines
   - Governance section

2. Updated the plan template at `.specify/templates/plan-template.md` to include a detailed constitution check section with compliance requirements for all core principles.

3. Updated the spec template at `.specify/templates/spec-template.md` to include functional requirements that align with the new constitution, particularly around JWT authentication, technology stack, and security requirements.

4. Updated the tasks template at `.specify/templates/tasks-template.md` to include foundational tasks that implement the constitutional requirements, such as JWT authentication setup, centralized API client, and user-based data isolation.

The constitution is now complete and all related templates have been updated to ensure consistency with the new principles. The constitution file includes a sync impact report at the top documenting the changes made.