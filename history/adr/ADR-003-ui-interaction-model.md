# ADR-003: UI Interaction Model

## Status

Accepted

## Date

2025-12-27

## Context

The Console Todo App requires a user interface approach that:

- Works purely in the terminal using `input()` and `print()`
- Is intuitive for users unfamiliar with command-line tools
- Supports progressive feature disclosure (basic → advanced)
- Handles partial task ID input for convenience
- Provides clear feedback and error messages

Constitution constraints:
- Must use pure console/CLI (no GUI frameworks)
- No web servers or HTTP endpoints
- Clear, actionable error messages
- Confirmation prompts for destructive operations

## Decision

We adopt a **menu-driven interface** with the following characteristics:

**Menu System:**
- Numbered menu options (1-18) displayed on each iteration
- Progressive feature levels: Level 1 (MVP: 1-6), Level 2 (7-12), Level 3 (13-18)
- Help command (`h`) available at all times
- Exit options: `0`, `q`, `quit`, `exit`

**Task Identification:**
- Full UUID generated for each task (36 characters)
- Short ID display: first 8 characters shown in lists
- Partial ID matching: user can enter 4+ characters if unique
- Ambiguous ID detection with helpful error message

**Input Handling:**
- Prompts use `InputHandler.prompt()` for consistent formatting
- Empty input handling per-context (skip, error, or keep current)
- Confirmation prompts for: delete task, bulk operations, import
- Default answer indicated by capital letter: `(y/N)`

**Display Formatting:**
- Fixed-width columns for task list (80 characters total)
- Separator lines for visual structure
- Legend explaining symbols shown after lists
- Truncation with `...` for long titles

**Error Communication:**
- Error prefix: `"Error: <message>"`
- No stack traces shown to users
- Actionable suggestions included (e.g., "Use 'list' to see all tasks")

## Consequences

**Positive:**
- Menu-driven is more discoverable than command parsing
- Numbered options reduce typing errors
- Partial ID matching reduces user friction
- Progressive levels prevent feature overwhelm
- Consistent prompt handling simplifies code

**Negative:**
- More verbose than command-line syntax (e.g., `todo add "Buy milk"`)
- Users must navigate menus for every operation
- No command history or auto-completion

**Risks:**
- Power users may find menu navigation slow
- Menu display overhead on each iteration

**Mitigations:**
- Quick command alternatives (0/q for exit, h for help)
- Clear, concise menu layout to minimize reading time

## Alternatives Considered

**1. Command-Line Parser (argparse style)**
- Pros: Familiar to CLI users, single-line operations, scriptable
- Cons: Steeper learning curve, requires remembering syntax
- Rejected: Menu-driven more accessible for general users

**2. REPL with Natural Language Commands**
- Pros: More intuitive command entry (e.g., "add task buy milk")
- Cons: Complex parsing, ambiguity handling, harder to implement
- Rejected: Over-engineering for this scope

**3. ncurses/TUI Full-Screen Interface**
- Pros: Rich interactive experience, vim-like navigation
- Cons: External dependency, platform compatibility issues
- Rejected: Constitution restricts to basic input()/print()

## References

- `IMPLEMENTATION_PLAN.md` - Section 4.2.5-4.2.7 (UI components)
- `constitution.md` - Section 5 (User Interface Specifications)
- `constitution.md` - Section 5.3 (Input Validation Messages)
- `constitution.md` - Section 5.4 (Confirmation Prompts)
