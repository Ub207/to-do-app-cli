# ADR-002: Application Architecture Pattern

## Status

Accepted

## Date

2025-12-27

## Context

The Console Todo App needs a clear architectural pattern that:

- Supports maintainability and testability
- Enables separation of concerns between UI and business logic
- Scales from basic MVP features to advanced functionality
- Allows individual components to be tested in isolation
- Follows Python best practices and PEP 8 guidelines

The constitution mandates:
- No global mutable state
- Small, single-purpose functions (<30 lines preferred)
- Clear separation of concerns
- Modular file structure

## Decision

We adopt a **layered architecture** with the following structure:

**Layer 1: Models** (`src/models/`)
- Pure data structures using `@dataclass`
- No business logic, only data representation
- Serialization/deserialization methods (to_dict, from_dict)
- Includes: `Task`, `Priority`

**Layer 2: Services** (`src/services/`)
- All business logic concentrated here
- `TaskService`: CRUD operations, filtering, sorting, search
- `StorageService`: JSON persistence, atomic writes, backup management
- Services receive dependencies via constructor (dependency injection)

**Layer 3: UI** (`src/ui/`)
- All user interaction isolated here
- `Menu`: Command routing and main loop
- `Display`: Output formatting
- `InputHandler`: Input prompts and validation
- Calls services but contains no business logic

**Layer 4: Utilities** (`src/utils/`)
- Shared pure functions
- `constants.py`: All magic values
- `validators.py`: Input validation functions
- `date_utils.py`: Date parsing and formatting

**Orchestration:**
- `main.py`: Entry point (<50 lines)
- `src/app.py`: Application bootstrap and signal handling
- Creates and wires all components together

## Consequences

**Positive:**
- Clear boundaries between components
- Services are easily unit testable without UI
- UI changes don't affect business logic
- Easy to add new features by extending appropriate layer
- Dependency injection enables mock testing

**Negative:**
- More files and directories than a flat structure
- Small indirection cost for method calls across layers
- Must maintain import hierarchy (layers import only from below)

**Risks:**
- Over-engineering for a simple app
- Layer violations if not careful (UI accessing storage directly)

**Mitigations:**
- Keep layer boundaries explicit through `__init__.py` exports
- Code review checklist includes layer compliance check

## Alternatives Considered

**1. Single Module Approach**
- Pros: Simpler, fewer files, faster initial development
- Cons: Becomes unmaintainable as features grow, hard to test
- Rejected: Constitution requires separation of concerns

**2. MVC Pattern**
- Pros: Well-known pattern, clear separation
- Cons: Controller concept awkward for CLI, model-view binding unnecessary
- Rejected: Services + UI layers better match CLI interaction model

**3. Command Pattern with Handlers**
- Pros: Clean command dispatch, easy to add commands
- Cons: More boilerplate, overkill for menu-driven interface
- Rejected: Menu-driven UI already provides command routing

## References

- `IMPLEMENTATION_PLAN.md` - Section 1.1 (Directory Layout)
- `constitution.md` - Section 3.3 (File Structure)
- `constitution.md` - Section 3.4 (Module Responsibilities)
