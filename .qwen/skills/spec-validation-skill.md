# Spec Validation Skill

**Purpose**: Ensure specifications are complete, consistent, and Phase-II ready.

## Actions
- Detect missing requirements
- Detect conflicting rules
- Verify authentication and authorization clarity
- Confirm frontend and backend responsibilities are defined

## Output
- Validation report
- List of issues that must be resolved before planning

## Rules
- Block implementation if critical gaps exist
- Do not write code

## Validation Checklist

### 1. Completeness Check
- [ ] All user stories have clear acceptance criteria
- [ ] Functional requirements are specific and testable
- [ ] Non-functional requirements are defined (performance, security, etc.)
- [ ] Edge cases and error scenarios are addressed
- [ ] Data entities and their relationships are clearly defined

### 2. Consistency Check
- [ ] No conflicting requirements exist
- [ ] All dependencies are clearly stated
- [ ] API contracts are consistent between frontend and backend
- [ ] Authentication and authorization rules are coherent

### 3. Phase-II Readiness Check
- [ ] Frontend responsibilities clearly defined
- [ ] Backend responsibilities clearly defined
- [ ] Integration points identified
- [ ] Security requirements specified
- [ ] Performance requirements defined

### 4. Critical Gaps to Block Implementation
- [ ] Missing authentication/authorization specifications
- [ ] Undefined data models or schemas
- [ ] Unclear API endpoints or contracts
- [ ] Missing error handling requirements
- [ ] Undefined success criteria

## Validation Report Template

### Summary
- **Spec Status**: [Complete/Incomplete/Requires Clarification]
- **Ready for Planning**: [Yes/No]
- **Critical Issues**: [Number]

### Issues Found
1. **[Issue Category]**: [Description]
   - **Impact**: [High/Medium/Low]
   - **Resolution Required**: [What needs to be done]

2. **[Issue Category]**: [Description]
   - **Impact**: [High/Medium/Low]
   - **Resolution Required**: [What needs to be done]

### Recommendations
- [Actionable recommendations to address issues]

### Next Steps
- [What needs to happen before planning can proceed]