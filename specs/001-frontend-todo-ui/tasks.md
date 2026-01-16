---

description: "Task list for Frontend Todo UI with Authentication implementation"
---

# Tasks: Frontend Todo UI with Authentication

**Input**: Design documents from `/specs/001-frontend-todo-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Next.js 16+ project structure in frontend/ directory
- [x] T002 Initialize TypeScript configuration with React 19+ support
- [x] T003 [P] Configure Tailwind CSS with Next.js App Router
- [x] T004 Setup project dependencies (Next.js, React, Better Auth, Tailwind CSS, Axios)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 [P] Configure Better Auth integration with Next.js App Router
- [x] T006 [P] Implement centralized API client in frontend/lib/api-client.ts with JWT token attachment
- [x] T007 Create type definitions in frontend/lib/types.ts for User Session, Task, Authentication Form, and Task Form
- [x] T008 Configure protected route handling with redirect to signin for unauthenticated users
- [x] T009 [P] Implement AuthContext and useAuth hook for session management
- [x] T010 Setup basic layout components (Header, Footer) in frontend/components/layout/
- [x] T011 Create base UI components (Button, Input, Card) in frontend/components/ui/
- [x] T012 Configure global styles and responsive design with Tailwind CSS

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register for an account and sign in to the todo application, and allow signed-in users to sign out.

**Independent Test**: Can be fully tested by registering a new account, signing in, and verifying access to the protected dashboard. This delivers the core value of a personalized todo application.

### Implementation for User Story 1

- [x] T013 [P] [US1] Create SignupForm component in frontend/components/auth/SignupForm.tsx
- [x] T014 [P] [US1] Create LoginForm component in frontend/components/auth/LoginForm.tsx
- [x] T015 [P] [US1] Create ProtectedRoute component in frontend/components/auth/ProtectedRoute.tsx
- [x] T016 [US1] Implement signup page at frontend/app/(auth)/signup/page.tsx
- [x] T017 [US1] Implement signin page at frontend/app/(auth)/signin/page.tsx
- [x] T018 [US1] Implement signout functionality in frontend/lib/auth.ts
- [x] T019 [US1] Add form validation to authentication forms
- [x] T020 [US1] Implement redirect after successful authentication to dashboard

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management Dashboard (Priority: P2)

**Goal**: Allow authenticated users to view, create, edit, and delete their tasks on a dashboard.

**Independent Test**: Can be fully tested by signing in, creating tasks, viewing them on the dashboard, editing existing tasks, and deleting tasks. This delivers the core todo management functionality.

### Implementation for User Story 2

- [x] T021 [P] [US2] Create TaskCard component in frontend/components/tasks/TaskCard.tsx
- [x] T022 [P] [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx
- [x] T023 [P] [US2] Create TaskForm component in frontend/components/tasks/TaskForm.tsx
- [x] T024 [US2] Implement dashboard page at frontend/app/(protected)/dashboard/page.tsx
- [x] T025 [US2] Implement API calls to fetch tasks from backend in frontend/hooks/useTasks.ts
- [x] T026 [US2] Implement task creation functionality with API integration
- [x] T027 [US2] Implement task editing functionality with API integration
- [x] T028 [US2] Implement task deletion functionality with API integration
- [x] T029 [US2] Add loading and error states to task operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Filtering and State Management (Priority: P3)

**Goal**: Provide task filtering capabilities and appropriate UI states (loading, empty, error) for better user experience.

**Independent Test**: Can be fully tested by signing in and observing how the application handles different states like loading, empty task lists, and error conditions. This delivers a robust and user-friendly experience.

### Implementation for User Story 3

- [x] T030 [P] [US3] Create EmptyState component in frontend/components/tasks/EmptyState.tsx
- [x] T031 [P] [US3] Create LoadingSpinner component in frontend/components/ui/LoadingSpinner.tsx
- [x] T032 [P] [US3] Create ErrorBoundary component in frontend/components/ui/ErrorBoundary.tsx
- [x] T033 [US3] Implement task filtering functionality in frontend/hooks/useTasks.ts
- [x] T034 [US3] Add empty state UI to dashboard when no tasks exist
- [x] T035 [US3] Add loading state UI during API requests
- [x] T036 [US3] Add error state UI for failed API requests
- [x] T037 [US3] Implement 401 Unauthorized handling with redirect to signin
- [x] T038 [US3] Add visual feedback for all user actions (success, error, loading states)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T039 [P] Add responsive design improvements across all components
- [x] T040 Add accessibility features to all UI components
- [x] T041 Implement proper error boundaries to handle unexpected errors gracefully
- [ ] T042 Add unit tests for critical components and hooks
- [ ] T043 Add integration tests for user flows
- [ ] T044 Run quickstart.md validation and update documentation as needed
- [ ] T045 Perform final code review and cleanup

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on authentication from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on authentication from US1 and task functionality from US2

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create SignupForm component in frontend/components/auth/SignupForm.tsx"
Task: "Create LoginForm component in frontend/components/auth/LoginForm.tsx"
Task: "Create ProtectedRoute component in frontend/components/auth/ProtectedRoute.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence