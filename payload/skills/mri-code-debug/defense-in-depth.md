# Defense-in-Depth Validation

## Overview

When you fix a bug caused by invalid data, adding validation at one place feels sufficient. But that single check can be bypassed by different code paths, refactoring, or mocks.

**Core principle:** Validate at EVERY layer data passes through. Make the bug structurally impossible.

## Why Multiple Layers

Single validation: "We fixed the bug"
Multiple layers: "We made the bug impossible"

Different layers catch different cases:
- Entry validation catches most bugs
- Business logic catches edge cases
- Environment guards prevent context-specific dangers
- Debug logging helps when other layers fail

## The Four Layers

### Layer 1: Entry Point Validation
**Purpose:** Reject obviously invalid input at the API boundary

```python
from pathlib import Path


def create_project(name: str, working_directory: str) -> None:
    if not working_directory or not working_directory.strip():
        raise ValueError("working_directory cannot be empty")
    wd = Path(working_directory)
    if not wd.exists():
        raise ValueError(f"working_directory does not exist: {working_directory}")
    if not wd.is_dir():
        raise ValueError(f"working_directory is not a directory: {working_directory}")
    # ... proceed
```

### Layer 2: Business Logic Validation
**Purpose:** Ensure data makes sense for this operation

```python
def initialize_workspace(project_dir: str, session_id: str) -> None:
    if not project_dir:
        raise ValueError("project_dir required for workspace initialization")
    # ... proceed
```

### Layer 3: Environment Guards
**Purpose:** Prevent dangerous operations in specific contexts

```python
import os
import tempfile
from pathlib import Path


def git_init(directory: str) -> None:
    # In tests, refuse `git init` outside temp directories.
    if os.environ.get("PYTEST_CURRENT_TEST"):
        target = Path(directory).resolve()
        tmp = Path(tempfile.gettempdir()).resolve()
        if tmp not in target.parents and target != tmp:
            raise RuntimeError(
                f"Refusing git init outside temp dir during tests: {directory}"
            )
    # ... proceed
```

### Layer 4: Debug Instrumentation
**Purpose:** Capture context for forensics

```python
import logging
import os
import traceback

logger = logging.getLogger(__name__)


def git_init(directory: str) -> None:
    logger.debug(
        "About to git init",
        extra={
            "directory": directory,
            "cwd": os.getcwd(),
            "stack": "".join(traceback.format_stack()),
        },
    )
    # ... proceed
```

## Applying the Pattern

When you find a bug:

1. **Trace the data flow** - Where does the bad value originate? Where is it used?
2. **Map all checkpoints** - List every point the data passes through
3. **Add validation at each layer** - Entry, business, environment, debug
4. **Test each layer** - Try to bypass layer 1, verify layer 2 catches it

## Example from a Session

Bug: an empty `project_dir` caused `git init` to run in the source tree.

**Data flow:**
1. Test setup → empty string
2. `create_project(name, "")`
3. `initialize_workspace("", ...)`
4. `git init` runs in `os.getcwd()`

**Four layers added:**
- Layer 1: `create_project()` validates not empty / exists / is a directory
- Layer 2: `initialize_workspace()` validates `project_dir` not empty
- Layer 3: environment guard refuses `git init` outside `tempfile.gettempdir()` in tests
- Layer 4: stack-trace logging before `git init`

**Result:** the whole suite passed and the bug became impossible to reproduce.

## Key Insight

All four layers were necessary. During testing, each layer caught bugs the others missed:
- Different code paths bypassed entry validation
- Mocks bypassed business logic checks
- Edge cases on different platforms needed environment guards
- Debug logging identified structural misuse

**Don't stop at one validation point.** Add checks at every layer.
