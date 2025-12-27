# ADR-004: Error Handling and Recovery Strategy

## Status

Accepted

## Date

2025-12-27

## Context

The Console Todo App must handle errors gracefully to:

- Never lose user data unexpectedly
- Provide clear, actionable feedback on errors
- Continue operating when possible despite failures
- Recover from corruption and external failures

Constitution requirements:
- Handle file not found gracefully (create new file)
- Handle JSON parsing errors gracefully
- Preserve data integrity on crash/interrupt
- Clear, non-technical error messages for user errors

## Decision

We adopt a **hierarchical exception strategy** with **graceful degradation**:

**Exception Hierarchy:**
```
TodoAppError (base)
├── ValidationError      # User input validation failures
├── TaskNotFoundError    # Task ID doesn't exist
├── AmbiguousIdError     # Partial ID matches multiple tasks
└── StorageError         # File operation failures
```

**Error Handling by Category:**

| Category | Strategy | User Message Pattern |
|----------|----------|---------------------|
| Invalid Input | Reject, guide | "Invalid input. Expected: <format>" |
| Task Not Found | Reject, suggest | "Task with ID '<id>' not found" |
| File Read Error | Recover | "Could not load tasks. Starting fresh." |
| File Write Error | Warn | "Warning: Could not save. Data may be lost." |
| Corrupted JSON | Backup + Reset | "Task file corrupted. Backed up and starting fresh." |
| Permission Denied | Degrade | "Cannot access file. Running in memory-only mode." |
| Unexpected | Continue | "An error occurred. Please try again." |

**Recovery Mechanisms:**

1. **Atomic Writes**: Write to `.tmp`, then rename to prevent partial writes
2. **Automatic Backup**: Create `.backup` before every save operation
3. **Corruption Recovery**: Copy corrupted file to `.corrupted.<timestamp>`, start fresh
4. **Memory-Only Fallback**: On permission errors, operate without persistence
5. **Signal Handling**: Catch SIGINT (Ctrl+C) for graceful exit with save

**Error Display Rules:**
- Never show Python tracebacks to users
- Prefix errors with "Error: " for visibility
- Include suggestion when applicable
- Use "Warning: " for non-fatal issues

## Consequences

**Positive:**
- Application remains usable even with storage failures
- No data loss during normal operation
- Users get actionable guidance on errors
- Backup files enable manual recovery
- Custom exceptions enable precise error handling

**Negative:**
- Memory-only mode loses changes on exit (users warned)
- Backup files consume additional disk space
- Multiple recovery paths add code complexity

**Risks:**
- Backup file proliferation over time
- Users may not notice memory-only mode warnings
- Corrupted backup could prevent recovery

**Mitigations:**
- Clear warning messages in memory-only mode
- Only backup on actual file overwrites
- Timestamp corrupted files for manual inspection

## Alternatives Considered

**1. Fail-Fast Approach**
- Pros: Simple, errors surface immediately
- Cons: Data loss on any failure, poor UX
- Rejected: Constitution requires graceful handling

**2. Transaction Log / WAL**
- Pros: Maximum data safety, incremental recovery
- Cons: Complex implementation, overkill for JSON file
- Rejected: Over-engineering for single-user app

**3. Auto-Retry with Exponential Backoff**
- Pros: Handles transient failures automatically
- Cons: Could block UI, unnecessary for local files
- Rejected: Local file operations either work or don't

## References

- `IMPLEMENTATION_PLAN.md` - Section 9 (Risk Mitigation)
- `IMPLEMENTATION_PLAN.md` - Section 9.2 (Safe Defaults)
- `IMPLEMENTATION_PLAN.md` - Section 9.3 (Recovery Procedures)
- `constitution.md` - Section 6 (Error Handling Specifications)
- `constitution.md` - Section 6.2 (Recovery Behavior)
