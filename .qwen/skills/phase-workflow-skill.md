# Phase Workflow Skill

**Purpose**: Enforce strict Spec-Kit Plus development phases.

## Phases
1. **sp.constitution** - Establish project principles and governance
2. **sp.specify** - Define feature specifications and requirements
3. **sp.plan** - Create architectural and implementation plan
4. **sp.tasks** - Break down work into testable tasks
5. **sp.implement** - Execute implementation based on approved tasks

## Actions
- Ensure phases are followed in order
- Prevent skipping or merging phases
- Confirm readiness before moving forward

## Rules
- Implementation is forbidden before sp.tasks approval
- Manual coding is not allowed

## Phase Validation Process

### 1. Phase Prerequisites Check
- [ ] Previous phase is completed and approved
- [ ] All required artifacts from previous phase exist
- [ ] No critical issues from previous phase remain unresolved
- [ ] Team has reviewed and approved previous phase output

### 2. Current Phase Readiness
- [ ] All required inputs for current phase are available
- [ ] No blocking issues from previous phase
- [ ] Resources are available to complete current phase
- [ ] Success criteria for current phase are defined

### 3. Phase Completion Criteria
- [ ] All required outputs for current phase are produced
- [ ] Outputs meet quality standards and completeness requirements
- [ ] Outputs have been reviewed and approved by relevant stakeholders
- [ ] Next phase prerequisites are satisfied

## Phase Transition Rules

### sp.constitution → sp.specify
- [ ] Project constitution is documented and approved
- [ ] Core principles are established
- [ ] Governance model is defined
- [ ] No unresolved constitutional issues

### sp.specify → sp.plan
- [ ] Complete feature specifications are available
- [ ] All requirements are clearly defined
- [ ] No critical gaps in specifications
- [ ] Specifications have been validated

### sp.plan → sp.tasks
- [ ] Architectural plan is complete and approved
- [ ] Technical approach is clearly defined
- [ ] Risks have been identified and mitigated
- [ ] Implementation strategy is viable

### sp.tasks → sp.implement
- [ ] Tasks are broken down into testable units
- [ ] Acceptance criteria are defined for each task
- [ ] No ambiguous requirements remain
- [ ] Tasks have been approved for implementation

## Enforcement Mechanisms

### 1. Phase Gate Reviews
- Each phase must be formally reviewed before proceeding
- Review includes all stakeholders
- Review outcomes are documented

### 2. Artifact Verification
- Automated checks for required artifacts
- Validation of artifact completeness
- Quality gates for each phase output

### 3. Blocking Implementation
- No code implementation allowed before sp.tasks approval
- Automated checks to prevent premature implementation
- Clear violation reporting

## Violation Handling
- **Phase Skipping**: Immediately halt and return to proper phase
- **Incomplete Artifacts**: Block progression until completion
- **Premature Implementation**: Rollback unauthorized changes
- **Missing Approvals**: Require proper review and approval

## Readiness Assessment Template

### Current Phase: [Phase Name]
### Status: [Ready/Blocked/In Progress]

### Prerequisites Met
- [ ] All previous phase artifacts completed
- [ ] All previous phase issues resolved
- [ ] Required inputs available
- [ ] Stakeholder approvals obtained

### Current Phase Completion
- [ ] Required outputs created
- [ ] Quality standards met
- [ ] Review completed
- [ ] Approval obtained

### Blockers
- [List any blockers preventing phase transition]

### Next Phase Readiness
- [ ] All current phase requirements satisfied
- [ ] Next phase prerequisites met
- [ ] Resources available for next phase