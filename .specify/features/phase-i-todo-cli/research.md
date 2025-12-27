# Phase I Research Notes

> Design decisions and research findings for Todo CLI (In-Memory)

---

## Research Summary

Phase I is intentionally minimal. All technical decisions are straightforward and use Python stdlib.

---

## Decision Log

### D-001: ID Generation Strategy

**Decision**: Use UUID v4 via `uuid.uuid4()`

**Rationale**:
- Guaranteed uniqueness without coordination
- Built into Python stdlib (`uuid` module)
- No external dependencies required
- Standard, well-understood format
- Can be truncated for user-friendly display

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Auto-increment integers | Requires state management for next ID |
| Timestamp-based | Collision risk in fast operations |
| Random strings | Custom implementation needed |
| NanoID | External dependency (forbidden) |

---

### D-002: In-Memory Storage Structure

**Decision**: Use Python `dict[str, Task]` with UUID as key

**Rationale**:
- O(1) lookup by ID
- O(n) iteration for listing (acceptable for in-memory)
- Built-in, no implementation needed
- Simple and maintainable
- Memory efficient for small task counts

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| List | O(n) lookup by ID |
| OrderedDict | Unnecessary, dict maintains insertion order in Python 3.7+ |
| Custom class | Over-engineering for Phase I |

---

### D-003: Timestamp Format

**Decision**: ISO 8601 string via `datetime.now().isoformat()`

**Rationale**:
- Human-readable
- Sortable as string
- Standard format
- No timezone complexity (local time sufficient for Phase I)
- Easy to format for display

**Format**: `"2024-12-27T10:30:45.123456"`

---

### D-004: Short ID Length

**Decision**: 8 characters (first 8 of UUID)

**Rationale**:
- Sufficient uniqueness for small task sets
- Human-readable and memorable
- Easy to type
- Matches common practice (Git commits use 7-8 chars)

**Collision Analysis**:
- 8 hex chars = 16^8 = 4.29 billion combinations
- For 100 tasks: collision probability ≈ 0.0000012%
- Acceptable for in-memory, single-session use

---

### D-005: Partial ID Resolution

**Decision**: Prefix matching with minimum 4 characters

**Rationale**:
- User convenience (don't need full UUID)
- 4 chars minimum prevents overly broad matches
- Simple `startswith()` matching
- Clear error messages for ambiguous matches

**Algorithm**:
```python
matches = [t for t in tasks if t.id.startswith(partial)]
if len(matches) == 0: raise TaskNotFoundError
if len(matches) > 1: raise AmbiguousIdError
return matches[0]
```

---

### D-006: Layer Architecture

**Decision**: 3-layer architecture (UI → Service → Model)

**Rationale**:
- Clear separation of concerns
- Testable service layer
- UI can be replaced without changing logic
- Follows constitution's clean architecture principle
- Not over-engineered for Phase I scope

**Layers**:
1. **UI**: Input/Output only (`menu.py`, `display.py`, `input_handler.py`)
2. **Service**: Business logic and storage (`task_service.py`)
3. **Model**: Data structure (`task.py`)

---

### D-007: Error Handling Approach

**Decision**: Custom exception hierarchy with catch-all in menu loop

**Rationale**:
- Specific error types for specific conditions
- Single catch point in UI layer
- User-friendly messages (no stack traces)
- Graceful recovery (return to menu)
- Follows Python conventions

**Hierarchy**:
```
TodoAppError (base)
├── TaskNotFoundError
├── AmbiguousIdError
└── ValidationError
```

---

### D-008: Input Handling

**Decision**: Centralized `InputHandler` class with static methods

**Rationale**:
- Single point for all `input()` calls
- Consistent whitespace handling
- Easy to test/mock
- Clear interface for UI layer

**Methods**:
- `prompt(message)` → stripped string
- `menu_choice()` → lowercase choice
- `confirm(message)` → boolean

---

## No Research Needed

The following were straightforward decisions requiring no research:

| Item | Decision | Reason |
|------|----------|--------|
| Language | Python 3.10+ | Constitution mandates |
| Dependencies | stdlib only | Constitution mandates |
| Persistence | None | Phase I scope |
| Testing | unittest | stdlib, adequate for scope |
| Code style | PEP 8 | Constitution mandates |

---

## Open Questions

None. All design decisions are finalized.

---

## References

- Python `uuid` module: https://docs.python.org/3/library/uuid.html
- Python `dataclasses`: https://docs.python.org/3/library/dataclasses.html
- Python `datetime`: https://docs.python.org/3/library/datetime.html
- PEP 8: https://peps.python.org/pep-0008/
