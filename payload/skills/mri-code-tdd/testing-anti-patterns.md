# Testing Anti-Patterns

**Load this reference when:** writing or changing tests, adding mocks, or tempted to add test-only methods to production code.

## Overview

Tests must verify real behavior, not mock behavior. Mocks are a means to isolate, not the thing being tested.

**Core principle:** Test what the code does, not what the mocks do.

**Following strict TDD prevents these anti-patterns.**

## The Iron Laws

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

## Anti-Pattern 1: Testing Mock Behavior

**The violation:**
```python
# ❌ BAD: the only assertion checks that the mock was called
def test_sends_welcome_email():
    mailer = Mock()
    register_user("alice@example.com", mailer=mailer)
    mailer.send.assert_called_once()   # proves the mock ran, not that a user was welcomed
```

**Why this is wrong:**
- You're verifying the mock works, not that the code works
- The test passes whenever the mock is wired up, regardless of real behavior
- It tells you nothing about the actual outcome

**Your human partner's correction:** "Are we testing the behavior of a mock?"

**The fix:**
```python
# ✅ GOOD: assert the real outcome, with a simple real double
def test_sends_welcome_email():
    outbox = InMemoryMailer()          # a real, in-memory test double
    register_user("alice@example.com", mailer=outbox)
    assert outbox.messages[0].to == "alice@example.com"
    assert "welcome" in outbox.messages[0].subject.lower()
```

### Gate Function

```
BEFORE asserting only that a mock was called:
  Ask: "Am I testing real behavior or just that the mock ran?"

  IF testing that the mock ran:
    STOP - assert the real outcome instead, or use a real test double

  Test real behavior instead
```

## Anti-Pattern 2: Test-Only Methods in Production

**The violation:**
```python
# ❌ BAD: destroy() only exists for tests
class Session:
    def destroy(self):  # looks like a production API!
        if self._workspace_manager:
            self._workspace_manager.destroy_workspace(self.id)
        # ... cleanup

# in tests
@pytest.fixture
def session():
    s = Session(...)
    yield s
    s.destroy()
```

**Why this is wrong:**
- Production class polluted with test-only code
- Dangerous if accidentally called in production
- Violates YAGNI and separation of concerns
- Confuses object lifecycle with entity lifecycle

**The fix:**
```python
# ✅ GOOD: test utilities handle test cleanup
# Session has no destroy() — it's stateless in production

# tests/utils.py
def cleanup_session(session):
    workspace = session.get_workspace_info()
    if workspace:
        workspace_manager.destroy_workspace(workspace.id)

# in tests
@pytest.fixture
def session():
    s = Session(...)
    yield s
    cleanup_session(s)
```

### Gate Function

```
BEFORE adding any method to a production class:
  Ask: "Is this only used by tests?"

  IF yes:
    STOP - Don't add it
    Put it in test utilities instead

  Ask: "Does this class own this resource's lifecycle?"

  IF no:
    STOP - Wrong class for this method
```

## Anti-Pattern 3: Mocking Without Understanding

**The violation:**
```python
# ❌ BAD: the stub removes a side effect the test depends on
def test_detects_duplicate_server(monkeypatch):
    # stubbing discover_and_cache prevents the config write the test needs!
    monkeypatch.setattr(ToolCatalog, "discover_and_cache_tools", lambda self: None)

    add_server(config)
    add_server(config)   # should raise DuplicateServerError — but won't
```

**Why this is wrong:**
- The stubbed method had a side effect the test depended on (writing config)
- Over-mocking to "be safe" breaks actual behavior
- The test passes for the wrong reason or fails mysteriously

**The fix:**
```python
# ✅ GOOD: mock at the correct level
def test_detects_duplicate_server(monkeypatch):
    # mock only the slow part (server startup); keep the config write
    monkeypatch.setattr(MCPServerManager, "start", lambda self: None)

    add_server(config)               # config written
    with pytest.raises(DuplicateServerError):
        add_server(config)           # duplicate detected ✓
```

### Gate Function

```
BEFORE mocking any method:
  STOP - Don't mock yet

  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF it depends on side effects:
    Mock at a lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what the test depends on:
    Run the test with the real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

## Anti-Pattern 4: Incomplete Mocks

**The violation:**
```python
# ❌ BAD: partial mock - only the fields you think you need
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"},
    # Missing: metadata that downstream code uses
}

# Later: breaks when code accesses response["metadata"]["request_id"]
```

**Why this is wrong:**
- **Partial mocks hide structural assumptions** - You only mocked fields you know about
- **Downstream code may depend on fields you didn't include** - Silent failures
- **Tests pass but integration fails** - Mock incomplete, real API complete
- **False confidence** - Test proves nothing about real behavior

**The Iron Rule:** Mock the COMPLETE data structure as it exists in reality, not just the fields your immediate test uses.

**The fix:**
```python
# ✅ GOOD: mirror the real API completely
mock_response = {
    "status": "success",
    "data": {"user_id": "123", "name": "Alice"},
    "metadata": {"request_id": "req-789", "timestamp": 1234567890},
    # all fields the real API returns
}
```

### Gate Function

```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"

  Actions:
    1. Examine an actual API response from docs/examples
    2. Include ALL fields the system might consume downstream
    3. Verify the mock matches the real response schema completely

  Critical:
    If you're creating a mock, you must understand the ENTIRE structure
    Partial mocks fail silently when code depends on omitted fields

  If uncertain: include all documented fields
```

## Anti-Pattern 5: Tests as an Afterthought

**The violation:**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```

**Why this is wrong:**
- Testing is part of implementation, not an optional follow-up
- TDD would have caught this
- You can't claim complete without tests

**The fix:**
```
TDD cycle:
1. Write a failing test
2. Implement to pass
3. Refactor
4. THEN claim complete
```

## When Mocks Become Too Complex

**Warning signs:**
- Mock setup longer than the test logic
- Mocking everything to make the test pass
- Mocks missing methods the real components have
- Test breaks when the mock changes

**Your human partner's question:** "Do we need to be using a mock here?"

**Consider:** integration tests with real components are often simpler than complex mocks.

## TDD Prevents These Anti-Patterns

**Why TDD helps:**
1. **Write the test first** → Forces you to think about what you're actually testing
2. **Watch it fail** → Confirms the test checks real behavior, not mocks
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies** → You see what the test actually needs before mocking

**If you're testing mock behavior, you violated TDD** - you added mocks without watching the test fail against real code first.

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert only that a mock was called | Assert the real outcome, or use a real test double |
| Test-only methods in production | Move to test utilities |
| Mock without understanding | Understand dependencies first, mock minimally |
| Incomplete mocks | Mirror the real API completely |
| Tests as afterthought | TDD - tests first |
| Over-complex mocks | Consider integration tests |

## Red Flags

- The only assertion is `mock.assert_called*` / `mock.called`
- Methods only called in test files
- Mock setup is >50% of the test
- Test fails when you remove the mock
- Can't explain why the mock is needed
- Mocking "just to be safe"

## The Bottom Line

**Mocks are tools to isolate, not things to test.**

If TDD reveals you're testing mock behavior, you've gone wrong.

Fix: test real behavior or question why you're mocking at all.
