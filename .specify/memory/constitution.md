<!--
Sync Impact Report
==================
Version Change: 1.1.0 → 2.0.0
Amendment Type: MAJOR (structural reorganization into article-based format)

Structural Changes:
- Reorganized from section-based to article-based format
- Enhanced with formal legal-style governance structure
- All principles preserved and strengthened

Modified Principles:
- Restructured into 8 Articles (was 10 Sections)
- Enhanced enforcement language and clarity
- Added explicit violation remediation procedures

Added Content:
- Article-based hierarchical structure
- Stronger enforcement language
- Explicit invalidity clauses for violations
- Self-validation requirements for agents

Removed Sections: None (all content preserved and reorganized)

Templates Requiring Updates:
- ⚠ .specify/templates/spec-template.md (to be created - add TDD section)
- ⚠ .specify/templates/plan-template.md (to be created - add traceability matrix)
- ⚠ .specify/templates/tasks-template.md (to be created - add task-to-spec mapping)

Rationale for MAJOR bump:
- Fundamental structural change from sections to articles
- Enhanced governance model (legal-style constitution)
- Stronger enforcement mechanisms
- All existing specs/plans remain valid (backward compatible in substance)

Follow-up TODOs:
- Create template files in .specify/templates/ directory
- Update any documentation referencing section numbers to article numbers
-->

# 🌐 Global Constitution
## Evolution of Todo — Unified Governance Framework

> **Supreme Governing Document** — All agents, specifications, plans, and code MUST comply.
> This constitution governs Phase I through Phase V of the Evolution of Todo project.
> No exceptions. No deviations. No overrides.

---

## Document Governance

| Attribute | Value |
|-----------|-------|
| **Version** | 2.0.0 |
| **Ratification Date** | 2024-12-27 |
| **Last Amended** | 2025-12-29 |
| **Scope** | Phase I through Phase V |
| **Authority** | Supreme — overrides all other documents |
| **Structure** | Article-based legal constitution |

---

## Article 1 — Supreme Law

### 1.1 Constitutional Authority

This Constitution is the highest governing authority over the entire Evolution of Todo project.

**All entities must comply:**
- All agents (AI and automated systems)
- All workflows and processes
- All systems, tools, and components
- All specifications, plans, and tasks
- All code and implementation artifacts

### 1.2 Supremacy Clause

```
No entity (human, agent, script, or subsystem) may override, bypass, or ignore this constitution.
```

**Supremacy Rules:**
```
MUST: All work complies with constitutional principles
MUST: Conflicts resolve in favor of the Constitution
MUST: Violations are immediately corrected through proper procedures
MUST NOT: Any document contradicts constitutional mandates
MUST NOT: Any agent bypasses constitutional requirements
MUST NOT: Any human overrides constitution without formal amendment
```

### 1.3 Invalidity of Non-Compliance

```
Violations are invalid and must be immediately corrected through proper constitutional
compliance procedures.
```

Any output, decision, or artifact that violates this constitution is:
- **Legally invalid** within the project governance framework
- **Subject to immediate remediation**
- **Not eligible for production deployment**
- **Requiring constitutional compliance review**

---

## Article 2 — Mandatory Spec-Driven Development

Spec-Driven Development is the **only legal execution model** for this project.

### 2.1 Development Hierarchy (Must Always Be Followed)

```
Constitution → Specifications → Plans → Tasks → Implementation
     ↑                                              |
     └──────────── Feedback Loop ──────────────────┘
```

**Hierarchy Rules:**
```
LEVEL 1 (Supreme):    Constitution - Immutable principles
LEVEL 2 (Strategic):  Specifications - WHAT to build
LEVEL 3 (Tactical):   Plans - HOW to build
LEVEL 4 (Execution):  Tasks - Atomic work units
LEVEL 5 (Output):     Implementation - Code artifacts
```

Each level MUST be approved before proceeding to the next level.

### 2.2 The Golden Rule

```
NO CODE SHALL BE WRITTEN WITHOUT AN APPROVED SPECIFICATION AND TASK LIST.
```

### 2.3 Development Execution Rules

No agent may implement code without:

1. **Approved Specification**
   - Feature requirements documented
   - Acceptance criteria defined
   - Success criteria established
   - Human approval obtained

2. **Approved Execution Plan**
   - Architecture decisions documented
   - Component design completed
   - Traceability matrix established
   - Human approval obtained

3. **Approved Task Breakdown**
   - Atomic, testable tasks defined
   - Each task references spec requirements
   - Test-first approach mandated
   - Tasks validated and approved

### 2.4 Human Developer Restrictions

```
No human developer is allowed to manually introduce logic, features, or structure
outside authorized tasks.
```

**Human Roles:**
```
ALLOWED:
  - Supervise and approve specifications
  - Review and approve plans
  - Validate and approve tasks
  - Review implementation for compliance
  - Conduct governance oversight

FORBIDDEN:
  - Write production code directly
  - Implement features without specs
  - Bypass the development hierarchy
  - Make architectural decisions without plan approval
  - Override agent execution without constitutional procedure
```

### 2.5 Ambiguity Resolution

```
Any ambiguity must be resolved by updating specifications, not writing experimental code.
```

**Resolution Process:**
1. Identify ambiguity or gap in specification
2. Stop implementation work
3. Document the ambiguity with context
4. Update specification to resolve ambiguity
5. Obtain approval for updated specification
6. Resume implementation with clarity

---

## Article 3 — Agent Behavior Governance

### 3.1 Behavioral Mandates

All agents must:

```
MUST: Follow approved specifications only
MUST: Execute only assigned and validated tasks
MUST: Maintain full traceability of actions
MUST: Request clarification when specifications are ambiguous
MUST: Stop and report when encountering specification gaps
MUST: Document all decisions with rationale
MUST: Self-validate constitutional compliance before output
MUST: Write tests BEFORE implementation code (TDD mandate)
```

### 3.2 Prohibited Behaviors

```
❌ No manual human coding intervention (agents execute, humans supervise)
❌ No unauthorized feature invention
❌ No deviation from approved specifications
❌ No implementing unplanned or unapproved architectural changes
❌ No bypassing reviews, approvals, or governance
❌ No "nice to have" features not explicitly specified
❌ No premature optimization without specification requirement
❌ No implementation code before tests exist
```

### 3.3 Refinement Policy

**Refinements are allowed only at the SPECIFICATION LEVEL**

```
MUST: All refinements occur at the specification level
MUST: Code changes require specification updates FIRST
MUST: Bug fixes that change behavior require spec amendment
MUST NOT: Refine or "improve" code beyond task requirements
MUST NOT: Add error handling, logging, or features not specified
```

**Code refinement without spec updates is strictly prohibited.**

### 3.4 Traceability Requirements

Every artifact in the development chain MUST be traceable:

```
MUST: Each task references its parent specification section (e.g., "US-001", "AC-003")
MUST: Each code commit references the task ID it implements
MUST: Each test references the requirement it validates
MUST: Specifications include unique identifiers for all requirements
MUST: Plans reference the spec requirements they address
MUST NOT: Create orphaned tasks without spec references
MUST NOT: Implement code that cannot be traced to a requirement
```

**Traceability Chain:**
```
Spec US-001 → Plan Section 3.2 → Task T-001 → Commit abc123 → Test test_us001_add_task
```

---

## Article 4 — Phase Governance

Phases are independent, strictly isolated governance units.

### 4.1 Phase Boundary Rules

```
Each phase operates only within its approved scope.
Future-phase functionality must never appear in earlier phases.
```

**Isolation Rules:**
```
MUST: Each phase has its own specification document
MUST: Phase N features MUST NOT appear in Phase N-1 implementation
MUST: Phase transitions require explicit approval
MUST NOT: Implement future-phase features in current phase
MUST NOT: "Prepare" for future phases without specification
MUST NOT: Add abstractions for unspecified future needs
```

### 4.2 Architecture Evolution

Architectures may evolve **only if:**

1. **Specifications update** - Feature requirements change
2. **Plans update** - Architecture decisions are revised
3. **Tasks update** - Implementation steps are regenerated
4. **Governance approves** - Human supervision validates changes

### 4.3 Phase Scope Definitions

#### Phase I: Todo CLI (In-Memory)
```
ALLOWED:
  - Console input/output only
  - In-memory task storage (session-scoped)
  - Basic CRUD operations
  - Simple data structures
  - Python standard library only

FORBIDDEN:
  - File persistence
  - Database connections
  - Network access
  - External dependencies beyond stdlib
```

#### Phase II: Persistent Todo
```
ALLOWED:
  - Everything from Phase I
  - File-based persistence (JSON/SQLite)
  - Data validation
  - Basic error recovery

FORBIDDEN:
  - Remote databases
  - API endpoints
  - Web interfaces
  - External services
```

#### Phase III: Todo API
```
ALLOWED:
  - Everything from Phase II
  - RESTful API endpoints
  - FastAPI framework
  - SQLModel ORM
  - Neon DB (PostgreSQL)
  - Authentication basics

FORBIDDEN:
  - Frontend code
  - Real-time features
  - AI/ML integrations
  - Message queues
```

#### Phase IV: Todo Web
```
ALLOWED:
  - Everything from Phase III
  - Next.js frontend
  - Full-stack integration
  - User authentication
  - Docker containerization

FORBIDDEN:
  - AI agents
  - Event streaming
  - Microservices architecture
  - Kubernetes deployment
```

#### Phase V: AI Todo
```
ALLOWED:
  - Everything from Phase IV
  - OpenAI Agents SDK
  - Model Context Protocol (MCP)
  - Kafka event streaming
  - Dapr for microservices
  - Kubernetes orchestration
  - Full cloud-native architecture
```

### 4.4 Immutable Phase Compliance

```
Phase scope violations invalidate the output.
Backporting from future phases is prohibited unless constitutionally amended.
```

**Violation Consequences:**
- Implementation is constitutionally invalid
- Must be remediated to phase-appropriate scope
- Cannot proceed to production
- Requires specification and plan revision

---

## Article 5 — Technology Constitution

The following technologies are constitutionally mandated.

### 5.1 Approved Technology Stack

| Layer | Phase I | Phase II | Phase III | Phase IV | Phase V |
|-------|---------|----------|-----------|----------|---------|
| **Language** | Python 3.10+ | Python 3.10+ | Python 3.10+ | Python + TypeScript | Python + TypeScript |
| **Backend** | - | - | **FastAPI** | **FastAPI** | **FastAPI** |
| **Data Layer** | - | - | **SQLModel** | **SQLModel** | **SQLModel** |
| **Database** | - | JSON/SQLite | **Neon DB** | **Neon DB** | **Neon DB** |
| **Frontend** | - | - | - | **Next.js** | **Next.js** |
| **Intelligence** | - | - | - | - | **OpenAI Agents SDK, MCP** |
| **Messaging** | - | - | - | - | **Kafka** |
| **Orchestration** | - | - | - | - | **Dapr** |
| **Containers** | - | - | - | **Docker** | **Docker, Kubernetes** |

### 5.2 Technology Mandates by Category

#### 5.2.1 Backend
- **Python** (all phases)
- **FastAPI** (Phase III+)

#### 5.2.2 Data Layer
- **SQLModel** (Phase III+)
- **Neon Database** (Phase III+)

#### 5.2.3 Intelligence & Orchestration
- **OpenAI Agents SDK** (Phase V)
- **Model Context Protocol (MCP)** (Phase V)

#### 5.2.4 Frontend
- **Next.js** (Phase IV+)

#### 5.2.5 Cloud & Distributed Systems
- **Docker** (Phase IV+)
- **Kubernetes** (Phase V)
- **Kafka** (Phase V)
- **Dapr** (Phase V)

### 5.3 Technology Stability Rules

```
Technology stack cannot change unless:
  1. Constitution is formally amended
  2. Specifications updated to reflect new technology
  3. Plans updated with new architectural decisions
  4. Governance approves the technology change
```

### 5.4 Dependency Rules

```
MUST: Use only technologies listed for current phase
MUST: Pin all dependency versions
MUST: Document reason for each external dependency
MUST: Prefer Python standard library when sufficient
MUST: Justify external dependencies in specification
MUST NOT: Add dependencies not in approved stack
MUST NOT: Use alpha/beta versions in production code
MUST NOT: Add dependencies "just in case"
```

### 5.5 Explicit Standards Policy

```
MUST: Define project-specific patterns explicitly in specifications
MUST: Document deviations from common standards (e.g., PEP 8 exceptions)
MUST NOT: Reference external standards without explicit project adoption
MUST NOT: Assume compliance with entire standard when only subset is used
MUST NOT: Let agents infer standards from incomplete documentation
```

**Rationale:** Agents cannot distinguish between full and partial standard adoption.
Be explicit about what patterns the project actually follows to prevent
implementation drift and over-compliance with unused standard sections.

---

## Article 6 — Quality & Engineering Principles

All work must comply with clean engineering principles.

### 6.1 Clean Engineering Mandates

```
MUST: Clean Architecture principles
MUST: Modularity in all components
MUST: Extensibility for future evolution
MUST: Maintainability for long-term sustainability
```

### 6.2 Separation of Concerns

The following layers **must remain separate and never entangled:**

1. **Presentation Layer**
   - User interface
   - Input handling
   - Output formatting

2. **Business Logic Layer**
   - Domain models
   - Business rules
   - Use cases

3. **Data Layer**
   - Persistence mechanisms
   - Data access
   - Storage abstractions

4. **Orchestration Layer** (Phase V)
   - Service coordination
   - Event handling
   - Workflow management

**Separation Rules:**
```
MUST: Separate concerns into distinct layers
MUST: Dependencies point inward (domain at center)
MUST: Business logic independent of frameworks
MUST: External interfaces are adapters only
MUST NOT: Mix business logic with I/O operations
MUST NOT: Couple domain models to persistence details
```

### 6.3 Code Quality Standards

```
MUST: Follow PEP 8 for Python code
MUST: Use type hints for all function signatures
MUST: Write docstrings for all public interfaces
MUST: Keep functions under 30 lines (prefer < 20)
MUST: Single responsibility per function/class
MUST NOT: Use magic numbers or hardcoded strings
MUST NOT: Leave commented-out code
MUST NOT: Use global mutable state
```

### 6.4 Stateless & Cloud-Native Principles

```
MUST: Services are stateless where specified (Phase III+)
MUST: State lives in databases or caches only
MUST: Each request is independent
MUST: Design for horizontal scaling (Phase III+)
MUST: Externalize configuration
MUST: Health check endpoints for services
MUST: Graceful shutdown handling
MUST: Structured logging (JSON format)
MUST NOT: Store session data in memory (after Phase I)
MUST NOT: Rely on request ordering
MUST NOT: Hardcode environment-specific values
MUST NOT: Assume single-instance deployment
```

**Cloud-Native Readiness:**
- **Scalability ready** - Can scale horizontally
- **Fault-tolerant readiness** - Handles failures gracefully
- **Deployment ready** - Can deploy to any cloud environment

### 6.5 Testing Requirements

| Type | Coverage | Requirement |
|------|----------|-------------|
| Unit Tests | 90%+ | MUST for all business logic |
| Integration Tests | Key paths | MUST for API endpoints |
| Contract Tests | API boundaries | MUST for service interfaces |
| E2E Tests | Critical flows | SHOULD for user journeys |

### 6.6 Test-Driven Development (TDD) Mandate

All implementation MUST follow strict Test-Driven Development practices:

```
MUST: Write tests BEFORE implementation code
MUST: Tests MUST be validated and approved by human supervisor
MUST: Tests MUST fail initially (Red phase) before implementation
MUST: Implementation MUST make tests pass (Green phase)
MUST: Refactoring MUST maintain passing tests
MUST NOT: Write implementation code before tests exist
MUST NOT: Skip the Red-Green-Refactor cycle
MUST NOT: Commit untested code
```

**TDD Workflow:**
```
1. RED Phase:
   - Write failing test based on specification requirement
   - Verify test fails for the right reason
   - Get human approval for test design

2. GREEN Phase:
   - Write minimal code to make test pass
   - Verify all tests pass
   - No refactoring in this phase

3. REFACTOR Phase:
   - Improve code structure without changing behavior
   - Maintain all passing tests
   - Document architectural decisions
```

---

## Article 7 — Stability & Permanence

### 7.1 Constitutional Stability

```
This Constitution remains stable across all phases.
It supersedes all specs, plans, and tasks.
Any contradictions must resolve in favor of the Constitution.
```

### 7.2 Conflict Resolution

**Resolution Hierarchy (Highest to Lowest):**
1. **Constitution** (Supreme)
2. **Specifications** (Strategic)
3. **Plans** (Tactical)
4. **Tasks** (Execution)
5. **Code** (Output)

In case of conflict:
- Lower-level artifacts MUST conform to higher-level artifacts
- Constitution always wins
- Update lower-level artifacts to resolve conflicts

### 7.3 Amendment Requirements

Updates require explicit constitutional amendment through this process:

**Amendment Procedure:**
```
1. PROPOSE amendment with detailed justification
2. ANALYZE impact on existing specifications and code
3. REVIEW by project stakeholders
4. APPROVE with documented rationale
5. UPDATE constitution with version increment
6. PROPAGATE changes to affected specifications
7. UPDATE templates and documentation
```

**Amendment Justifications (only valid reasons):**
1. A requirement fundamentally conflicts with project goals
2. A technical limitation makes a rule impossible
3. A security vulnerability requires immediate change
4. Phase requirements necessitate governance evolution

**Version Numbering:**
```
MAJOR (X.0.0): Incompatible governance changes, principle removals, structural changes
MINOR (0.X.0): New principles added, material expansions
PATCH (0.0.X): Clarifications, typo fixes, non-semantic changes
```

---

## Article 8 — Enforcement

### 8.1 Invalidity of Non-Compliance

```
Any non-compliant output is constitutionally invalid.
```

**Invalid Outputs Include:**
- Code without approved specifications
- Features not in approved specifications
- Architecture not in approved plans
- Tasks without specification references
- Implementations without tests (TDD violation)
- Phase violations (future-phase features in earlier phases)

### 8.2 Agent Self-Validation

```
Agents must self-validate constitutional compliance before producing output.
```

**Pre-Output Validation Checklist:**
- [ ] Specification exists and is approved
- [ ] Plan exists and is approved
- [ ] Task is approved and references specification
- [ ] Tests written before implementation (TDD)
- [ ] Phase scope compliance verified
- [ ] Technology stack compliance verified
- [ ] Traceability chain is complete
- [ ] No prohibited behaviors executed

### 8.3 Continuous Governance Enforcement

```
Governance agents must continuously enforce constitution alignment.
```

**Enforcement Mechanisms:**
- Pre-merge compliance validation
- Automated constitutional compliance checks
- Human governance oversight
- Periodic compliance audits

### 8.4 Remediation Process

When violations are detected:

**Appeals and Remediation Require:**

1. **Governance Review**
   - Identify nature and severity of violation
   - Assess impact on project integrity
   - Determine remediation path

2. **Spec Adjustment (if needed)**
   - Update specification to resolve ambiguity
   - Clarify requirements
   - Obtain approval for changes

3. **Constitutional Amendment (if required)**
   - Follow Article 7.3 amendment procedure
   - Justify need for constitutional change
   - Update all affected artifacts

### 8.5 Compliance Checklist

Before any code is merged, verify:

#### 8.5.1 Spec-Driven Compliance
- [ ] Feature has approved specification
- [ ] Implementation matches specification exactly
- [ ] No unspecified features added
- [ ] All tasks completed as defined
- [ ] Traceability chain is complete (spec → plan → task → code → test)

#### 8.5.2 Phase Compliance
- [ ] No future-phase features present
- [ ] Technology stack matches phase requirements
- [ ] Architecture aligns with phase scope

#### 8.5.3 Code Quality Compliance
- [ ] Type hints on all functions
- [ ] Docstrings on public interfaces
- [ ] PEP 8 compliance verified
- [ ] No forbidden patterns used
- [ ] Tests achieve coverage requirements

#### 8.5.4 Agent Compliance
- [ ] No invented features
- [ ] No spec deviations
- [ ] All decisions documented
- [ ] Refinements occurred at spec level
- [ ] No manual human coding (agent-executed only)

#### 8.5.5 TDD Compliance
- [ ] Tests written before implementation
- [ ] Tests initially failed (Red phase documented)
- [ ] All tests now pass (Green phase verified)
- [ ] Refactoring maintained test suite
- [ ] Each requirement has corresponding test

---

## ✅ Final Statement

**This Constitution governs the entire Evolution of Todo Project (Phase I → Phase V).**

It ensures:
- **Discipline** - Structured, spec-driven development
- **Structure** - Clear hierarchy and governance
- **Technological Consistency** - Approved stack across phases
- **Governance Integrity** - Constitutional compliance enforcement
- **High-Quality Engineering Outcomes** - Clean, tested, maintainable code

---

## Definitions

| Term | Definition |
|------|------------|
| **Constitution** | This document — supreme governing authority |
| **Specification** | Document defining what to build, with acceptance criteria |
| **Plan** | Document defining how to build, with architecture decisions |
| **Task** | Atomic unit of work that implements part of a specification |
| **Agent** | AI or automated system executing development tasks |
| **Phase** | Major project milestone with defined scope and technologies |
| **Traceability** | Ability to link each code element back to its requirement |
| **TDD** | Test-Driven Development — tests before implementation |
| **Governance** | Constitutional enforcement and compliance oversight |

---

*This constitution is the supreme law of the Evolution of Todo project.*
*All specifications, plans, tasks, and code MUST comply.*
*No agent may deviate. No human may override without amendment.*

**Version:** 2.0.0
**Ratification Date:** 2024-12-27
**Last Amendment:** 2025-12-29
**Effective:** Immediately and perpetually until amended
