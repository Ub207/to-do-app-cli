<!--
Sync Impact Report
==================
Version Change: N/A → 1.0.0
New Constitution: Created for "Evolution of Todo" project (Phase I-V)

Added Sections:
- Spec-Driven Development Mandate
- Agent Behavior Rules
- Phase Governance
- Technology Constraints (Phase I-V)
- Quality Principles
- Development Workflow
- Amendment & Governance

Templates Requiring Updates:
- ⚠ .specify/templates/spec-template.md (to be created)
- ⚠ .specify/templates/plan-template.md (to be created)
- ⚠ .specify/templates/tasks-template.md (to be created)

Follow-up TODOs: None
-->

# Constitution: Evolution of Todo

> **Supreme Governing Document** — All agents, specifications, plans, and code MUST comply.
> This constitution governs Phase I through Phase V of the Evolution of Todo project.
> No exceptions. No deviations. Spec-driven development is mandatory.

---

## Document Governance

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0.0 |
| **Ratification Date** | 2024-12-27 |
| **Last Amended** | 2024-12-27 |
| **Scope** | Phase I through Phase V |
| **Authority** | Supreme — overrides all other documents |

---

## 1. Project Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Evolution of Todo |
| **Type** | Multi-Phase Application (CLI → Web → AI-Powered) |
| **Philosophy** | Spec-Driven, Agent-Executed, Human-Supervised |
| **Governance Model** | Constitution → Specs → Plan → Tasks → Implement |

### 1.1 Phase Overview

| Phase | Name | Scope | Key Technologies |
|-------|------|-------|------------------|
| I | Todo CLI | In-memory console app | Python, CLI |
| II | Persistent Todo | File/DB persistence | Python, SQLite/JSON |
| III | Todo API | RESTful backend | FastAPI, SQLModel, Neon DB |
| IV | Todo Web | Full-stack application | Next.js, FastAPI |
| V | AI Todo | Intelligent agents | OpenAI Agents SDK, MCP, Kafka, Dapr |

---

## 2. Spec-Driven Development Mandate

This principle is **NON-NEGOTIABLE** and forms the foundation of all project work.

### 2.1 The Golden Rule

```
NO CODE SHALL BE WRITTEN WITHOUT AN APPROVED SPECIFICATION AND TASK LIST.
```

### 2.2 Mandatory Workflow

All work MUST follow this exact sequence:

```
Constitution → Specification → Plan → Tasks → Implementation
     ↑                                              |
     └──────────── Feedback Loop ──────────────────┘
```

| Stage | Document | Purpose | Gate |
|-------|----------|---------|------|
| 1 | Constitution | Supreme law, immutable principles | Always active |
| 2 | Specification (spec.md) | Feature requirements, acceptance criteria | MUST be approved |
| 3 | Plan (plan.md) | Architecture, design decisions | MUST be approved |
| 4 | Tasks (tasks.md) | Atomic implementation steps | MUST be complete |
| 5 | Implementation | Code that fulfills tasks | MUST pass tests |

### 2.3 Enforcement Rules

```
MUST: Every feature begins with a specification document
MUST: Specifications MUST be approved before planning begins
MUST: Plans MUST be approved before task generation
MUST: Tasks MUST be complete before implementation starts
MUST: All code MUST trace back to a specific task
MUST NOT: Write code without corresponding approved task
MUST NOT: Add features not in approved specification
MUST NOT: Skip any stage of the workflow
```

---

## 3. Agent Behavior Rules

These rules govern ALL agents (AI or automated) working on this project.

### 3.1 Core Agent Constraints

```
MUST: Follow the spec-driven workflow without exception
MUST: Request clarification when specifications are ambiguous
MUST: Stop and report when encountering specification gaps
MUST: Document all decisions with rationale
MUST NOT: Invent features not in specifications
MUST NOT: Make architectural decisions without spec/plan approval
MUST NOT: Deviate from approved specifications
MUST NOT: Implement "nice to have" features not explicitly specified
```

### 3.2 Refinement Rules

```
MUST: All refinements occur at the specification level
MUST: Code changes require specification updates FIRST
MUST: Bug fixes that change behavior require spec amendment
MUST NOT: Refine or "improve" code beyond task requirements
MUST NOT: Add error handling, logging, or features not specified
```

### 3.3 Human Interaction Rules

```
MUST: Humans supervise and approve specifications
MUST: Humans approve plans before task generation
MUST: Agents execute approved tasks only
MUST NOT: Humans write production code directly
MUST NOT: Agents accept verbal instructions without spec updates
```

---

## 4. Phase Governance

Each phase is strictly bounded by its specification. Cross-phase contamination is forbidden.

### 4.1 Phase Isolation Rules

```
MUST: Each phase has its own specification document
MUST: Phase N features MUST NOT appear in Phase N-1 implementation
MUST: Architecture may evolve ONLY through updated specs and plans
MUST: Phase transitions require explicit approval
MUST NOT: Implement future-phase features in current phase
MUST NOT: "Prepare" for future phases without specification
MUST NOT: Add abstractions for unspecified future needs
```

### 4.2 Phase Scope Definitions

#### Phase I: Todo CLI (In-Memory)
```
ALLOWED:
  - Console input/output only
  - In-memory task storage (session-scoped)
  - Basic CRUD operations
  - Simple data structures

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

---

## 5. Technology Constraints

### 5.1 Approved Technology Stack

| Layer | Phase I | Phase II | Phase III | Phase IV | Phase V |
|-------|---------|----------|-----------|----------|---------|
| Language | Python 3.10+ | Python 3.10+ | Python 3.10+ | Python + TypeScript | Python + TypeScript |
| Backend Framework | - | - | FastAPI | FastAPI | FastAPI |
| ORM | - | - | SQLModel | SQLModel | SQLModel |
| Database | - | JSON/SQLite | Neon DB | Neon DB | Neon DB |
| Frontend | - | - | - | Next.js | Next.js |
| AI/Agents | - | - | - | - | OpenAI Agents SDK, MCP |
| Messaging | - | - | - | - | Kafka |
| Microservices | - | - | - | - | Dapr |
| Containers | - | - | - | Docker | Docker, Kubernetes |

### 5.2 Dependency Rules

```
MUST: Use only technologies listed for current phase
MUST: Pin all dependency versions
MUST: Document reason for each external dependency
MUST NOT: Add dependencies not in approved stack
MUST NOT: Use alpha/beta versions in production code
MUST NOT: Add dependencies "just in case"
```

### 5.3 Standard Library Priority

```
MUST: Prefer Python standard library when sufficient
MUST: Justify external dependencies in specification
MUST: Minimize dependency tree depth
```

---

## 6. Quality Principles

### 6.1 Clean Architecture

```
MUST: Separate concerns into distinct layers
MUST: Dependencies point inward (domain at center)
MUST: Business logic independent of frameworks
MUST: External interfaces are adapters only
MUST NOT: Mix business logic with I/O operations
MUST NOT: Couple domain models to persistence details
```

### 6.2 Code Quality Standards

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

### 6.3 Stateless Services

```
MUST: Services are stateless where specified
MUST: State lives in databases or caches only
MUST: Each request is independent
MUST NOT: Store session data in memory (after Phase I)
MUST NOT: Rely on request ordering
```

### 6.4 Cloud-Native Readiness

```
MUST: Design for horizontal scaling (Phase III+)
MUST: Externalize configuration
MUST: Health check endpoints for services
MUST: Graceful shutdown handling
MUST: Structured logging (JSON format)
MUST NOT: Hardcode environment-specific values
MUST NOT: Assume single-instance deployment
```

### 6.5 Testing Requirements

| Type | Coverage | Requirement |
|------|----------|-------------|
| Unit Tests | 90%+ | MUST for all business logic |
| Integration Tests | Key paths | MUST for API endpoints |
| Contract Tests | API boundaries | MUST for service interfaces |
| E2E Tests | Critical flows | SHOULD for user journeys |

---

## 7. Development Workflow

### 7.1 Feature Development Sequence

```
1. CREATE specification (spec.md)
   └── Define requirements, acceptance criteria, constraints

2. REVIEW specification
   └── Human approval required

3. CREATE plan (plan.md)
   └── Architecture decisions, component design

4. REVIEW plan
   └── Human approval required

5. GENERATE tasks (tasks.md)
   └── Atomic, testable implementation steps

6. IMPLEMENT tasks
   └── Agent executes approved tasks only

7. TEST implementation
   └── All tests must pass

8. REVIEW code
   └── Verify compliance with spec and constitution
```

### 7.2 Change Management

```
To change existing functionality:
1. UPDATE specification first
2. GET approval for spec changes
3. UPDATE plan if architecture affected
4. REGENERATE affected tasks
5. IMPLEMENT changes
6. UPDATE tests

NEVER modify code without updating specs first.
```

---

## 8. Amendment Process

### 8.1 Constitution Amendments

This constitution may only be amended when:

1. A requirement fundamentally conflicts with project goals
2. A technical limitation makes a rule impossible
3. A security vulnerability requires immediate change
4. Phase requirements necessitate governance evolution

### 8.2 Amendment Procedure

```
1. PROPOSE amendment with detailed justification
2. ANALYZE impact on existing specifications and code
3. REVIEW by project stakeholders
4. APPROVE with documented rationale
5. UPDATE constitution with version increment
6. PROPAGATE changes to affected specifications
```

### 8.3 Version Numbering

```
MAJOR (X.0.0): Incompatible governance changes, principle removals
MINOR (0.X.0): New principles added, material expansions
PATCH (0.0.X): Clarifications, typo fixes, non-semantic changes
```

---

## 9. Compliance Checklist

Before any code is merged, verify:

### 9.1 Spec-Driven Compliance
- [ ] Feature has approved specification
- [ ] Implementation matches specification exactly
- [ ] No unspecified features added
- [ ] All tasks completed as defined

### 9.2 Phase Compliance
- [ ] No future-phase features present
- [ ] Technology stack matches phase requirements
- [ ] Architecture aligns with phase scope

### 9.3 Code Quality Compliance
- [ ] Type hints on all functions
- [ ] Docstrings on public interfaces
- [ ] PEP 8 compliance verified
- [ ] No forbidden patterns used
- [ ] Tests achieve coverage requirements

### 9.4 Agent Compliance
- [ ] No invented features
- [ ] No spec deviations
- [ ] All decisions documented
- [ ] Refinements occurred at spec level

---

## 10. Definitions

| Term | Definition |
|------|------------|
| **Specification** | Document defining what to build, with acceptance criteria |
| **Plan** | Document defining how to build, with architecture decisions |
| **Task** | Atomic unit of work that implements part of a specification |
| **Agent** | AI or automated system executing development tasks |
| **Phase** | Major project milestone with defined scope and technologies |
| **Constitution** | This document — supreme governing authority |

---

*This constitution is the supreme law of the Evolution of Todo project.*
*All specifications, plans, tasks, and code MUST comply.*
*No agent may deviate. No human may override without amendment.*

**Version:** 1.0.0
**Ratification Date:** 2024-12-27
**Effective:** Immediately and perpetually until amended
