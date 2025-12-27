# ADR-001: Data Model and Persistence Strategy

## Status

Accepted

## Date

2025-12-27

## Context

The Console Todo App requires a reliable way to store and retrieve task data that persists between application sessions. Key constraints from the constitution include:

- Pure console/CLI application (no database servers)
- Standard library only (except optional formatting libraries)
- Must handle file corruption gracefully
- Must preserve data integrity on crash/interrupt
- No network access or external services

The data model needs to support tasks with multiple attributes including priority, tags, due dates, and recurring patterns while remaining serializable and easy to extend.

## Decision

We adopt the following integrated approach for data modeling and persistence:

**Data Model:**
- Use Python `dataclasses` for the Task model with type hints
- Use Python `enum.Enum` for Priority levels (NONE, LOW, MEDIUM, HIGH)
- Use `uuid.uuid4()` for unique task identifiers
- Store timestamps as ISO 8601 strings for JSON compatibility

**Persistence:**
- Use JSON file format for human-readable, portable storage
- Store data in `data/tasks.json` by default
- Implement atomic writes: write to `.tmp` file, then rename
- Create `.backup` file before each write operation
- Include version field in JSON for future migration support

**Error Recovery:**
- On corrupted JSON: backup corrupted file with timestamp, start fresh
- On permission errors: fall back to memory-only mode with user warning
- On missing file: create new empty file structure

## Consequences

**Positive:**
- JSON is human-readable and easily editable manually if needed
- No external dependencies for storage
- Atomic writes prevent partial file corruption
- Backup files provide recovery option
- Memory-only fallback ensures app remains usable
- Dataclasses provide clear, type-safe data structures

**Negative:**
- JSON files can become large with many tasks (not suitable for >10,000 tasks)
- No concurrent access support (single-user only)
- Full file rewrite on every save (no incremental updates)
- String-based timestamps less efficient than native datetime objects

**Risks:**
- Large task lists may cause performance degradation
- Manual JSON edits could introduce corruption

## Alternatives Considered

**1. SQLite Database**
- Pros: Better performance for large datasets, concurrent access, querying
- Cons: Binary format not human-readable, additional complexity
- Rejected: Overkill for expected task volume, violates simplicity principle

**2. Plain Text Format**
- Pros: Maximally simple, easily editable
- Cons: No structure for complex data, parsing complexity
- Rejected: Cannot represent task metadata efficiently

**3. Pickle/Binary Serialization**
- Pros: Faster serialization, native Python objects
- Cons: Not human-readable, Python-version dependent, security concerns
- Rejected: Constitution requires JSON, binary formats not portable

## References

- `IMPLEMENTATION_PLAN.md` - Sections 3.1, 4.2.2, 5.2
- `constitution.md` - Section 2.4 (Data Persistence Rules)
- `constitution.md` - Section 3.1 (Core Data Model)
