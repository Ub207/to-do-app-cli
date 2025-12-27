# Phase I Data Model

> Entity definitions for Todo CLI (In-Memory)

---

## Entities

### Task

The single entity in Phase I.

```python
@dataclass
class Task:
    """
    Represents a todo task.

    All fields are immutable after creation except via service methods.
    """

    id: str
    # - Type: UUID v4 string
    # - Generated: Automatically on creation
    # - Format: "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    # - Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

    title: str
    # - Required: Yes
    # - Constraints: Non-empty, max 200 characters
    # - Validation: Strip whitespace, reject if empty

    description: str = ""
    # - Required: No
    # - Default: Empty string
    # - Constraints: Max 1000 characters
    # - Can be cleared by setting to ""

    completed: bool = False
    # - Required: Yes (has default)
    # - Default: False (pending)
    # - Toggled via toggle_complete()

    created_at: str
    # - Type: ISO 8601 timestamp string
    # - Generated: Automatically on creation
    # - Format: "YYYY-MM-DDTHH:MM:SS.ffffff"
    # - Immutable after creation

    updated_at: str
    # - Type: ISO 8601 timestamp string
    # - Generated: On creation and every update
    # - Format: "YYYY-MM-DDTHH:MM:SS.ffffff"
    # - Updated whenever task is modified
```

---

## Field Specifications

| Field | Type | Required | Default | Mutable | Constraints |
|-------|------|:--------:|---------|:-------:|-------------|
| `id` | `str` | Yes | Auto | No | UUID v4 format |
| `title` | `str` | Yes | - | Yes | Non-empty, ≤200 chars |
| `description` | `str` | No | `""` | Yes | ≤1000 chars |
| `completed` | `bool` | Yes | `False` | Yes | Via toggle only |
| `created_at` | `str` | Yes | Auto | No | ISO 8601 |
| `updated_at` | `str` | Yes | Auto | Yes | ISO 8601, auto-updated |

---

## Derived Properties

### short_id

```python
@property
def short_id(self) -> str:
    """First 8 characters of UUID for display."""
    return self.id[:8]
```

- Purpose: User-friendly ID display
- Example: `"a1b2c3d4"` from `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`

---

## State Transitions

### Completion Status

```
┌──────────┐  toggle_complete()  ┌───────────┐
│ Pending  │◄───────────────────►│ Completed │
│ (false)  │                     │ (true)    │
└──────────┘                     └───────────┘
```

### Task Lifecycle

```
Create                    Update(s)                    Delete
  │                          │                           │
  ▼                          ▼                           ▼
┌─────────┐    ┌─────────────────────────┐    ┌─────────────────┐
│ NEW     │───►│ ACTIVE                  │───►│ REMOVED         │
│         │    │ (can be modified)       │    │ (garbage        │
│ id=uuid │    │ updated_at changes      │    │  collected)     │
└─────────┘    └─────────────────────────┘    └─────────────────┘
```

---

## Storage Structure

### In-Memory Dictionary

```python
_tasks: dict[str, Task] = {}

# Key: Full UUID string
# Value: Task instance

# Example state:
{
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890": Task(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        title="Buy groceries",
        description="Milk, bread, eggs",
        completed=False,
        created_at="2024-12-27T10:30:45.123456",
        updated_at="2024-12-27T10:30:45.123456"
    ),
    "e5f6g7h8-i9j0-k1l2-mnop-qr3456789012": Task(
        id="e5f6g7h8-i9j0-k1l2-mnop-qr3456789012",
        title="Call dentist",
        description="",
        completed=True,
        created_at="2024-12-27T09:15:30.654321",
        updated_at="2024-12-27T11:00:00.000000"
    )
}
```

---

## Validation Rules

### Title Validation

```python
def validate_title(title: str) -> str:
    """
    Validate and normalize title.

    Args:
        title: Raw title input

    Returns:
        Normalized title (stripped)

    Raises:
        ValidationError: If title is empty after strip
    """
    normalized = title.strip()
    if not normalized:
        raise ValidationError("Title cannot be empty.")
    if len(normalized) > 200:
        raise ValidationError("Title must be 200 characters or less.")
    return normalized
```

### Description Validation

```python
def validate_description(description: str) -> str:
    """
    Validate and normalize description.

    Args:
        description: Raw description input

    Returns:
        Normalized description (stripped)

    Raises:
        ValidationError: If description exceeds max length
    """
    normalized = description.strip()
    if len(normalized) > 1000:
        raise ValidationError("Description must be 1000 characters or less.")
    return normalized
```

---

## NOT in Phase I

The following are explicitly excluded from the data model:

| Field | Phase | Reason |
|-------|-------|--------|
| `priority` | II | Not in spec |
| `tags` | II | Not in spec |
| `due_date` | II | Not in spec |
| `recurring` | II | Not in spec |
| `category` | II+ | Not in spec |
| `attachments` | III+ | Not in spec |
| `user_id` | III+ | Single user, no auth |
