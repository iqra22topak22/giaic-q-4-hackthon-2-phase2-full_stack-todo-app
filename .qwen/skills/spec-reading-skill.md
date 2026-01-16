# Spec Reading Skill

**Purpose**: Extract accurate and complete information from Spec-Kit documents.

## Input
- /specs/overview.md
- /specs/features/*
- /specs/api/*
- /specs/database/*
- /specs/ui/*

## Actions
- Read specs carefully without assumptions
- Identify requirements, constraints, and scope
- Highlight important rules and dependencies

## Output
- Clear summary of what must be built
- List of explicit constraints

## Rules
- Do not interpret beyond written specs
- Do not suggest implementation

## Reading Process

### 1. Document Discovery
- Locate all spec documents in the expected directories
- Identify the hierarchy and relationships between documents
- Note any missing documents that are referenced but not found

### 2. Information Extraction
- Extract functional requirements from user stories
- Identify non-functional requirements (performance, security, etc.)
- Capture API endpoints and their specifications
- Document data models and database schemas
- Note UI/UX requirements and constraints
- Identify dependencies between components

### 3. Constraint Identification
- Extract all explicit constraints mentioned in the specs
- Identify implicit constraints based on requirements
- Note any technology or platform limitations
- Capture performance and scalability requirements
- Document security and compliance requirements

### 4. Scope Definition
- Determine what is in scope for the current phase
- Identify out-of-scope items for future phases
- Clarify any ambiguous requirements
- Flag any requirements that need additional clarification

## Output Format

### Summary of What Must Be Built
- **Core Features**: [List of main features to implement]
- **Integration Points**: [List of external systems or services to integrate with]
- **User Interactions**: [Key user journeys and interactions]
- **Data Flow**: [How data moves through the system]

### Explicit Constraints
- **Technical Constraints**: [Technology stack, platform, performance limits]
- **Business Constraints**: [Regulatory, compliance, or business rule constraints]
- **Timeline Constraints**: [Any time-based limitations]
- **Resource Constraints**: [Any limitations on resources or infrastructure]

### Dependencies
- **External Dependencies**: [Third-party services, libraries, APIs]
- **Internal Dependencies**: [Other components or teams]
- **Data Dependencies**: [Required data sources or formats]

### Requirements Hierarchy
- **Must Have**: [Critical requirements for MVP]
- **Should Have**: [Important but not critical requirements]
- **Could Have**: [Nice-to-have features]
- **Won't Have**: [Explicitly excluded items]