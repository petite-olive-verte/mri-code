"""Condition-based waiting utilities — worked example.

Replaces arbitrary `time.sleep()` calls in tests with polling on the actual
condition. Built on the generic `wait_for` helper (see condition-based-waiting.md).

The `EventStore` protocol here stands in for whatever your code exposes — a queue,
a log, a message bus. Adapt `get_events` to your own accessor.
"""

import time
from typing import Callable, Protocol


class Event(Protocol):
    type: str
    data: dict


class EventStore(Protocol):
    def get_events(self, thread_id: str) -> list[Event]: ...


def wait_for_event(
    store: EventStore,
    thread_id: str,
    event_type: str,
    timeout: float = 5.0,
) -> Event:
    """Wait for the first event of `event_type` to appear.

    Example:
        wait_for_event(store, agent_thread_id, "TOOL_RESULT")
    """
    deadline = time.monotonic() + timeout
    while True:
        event = next(
            (e for e in store.get_events(thread_id) if e.type == event_type), None
        )
        if event is not None:
            return event
        if time.monotonic() > deadline:
            raise TimeoutError(
                f"Timeout waiting for {event_type} event after {timeout}s"
            )
        time.sleep(0.01)  # poll every 10ms


def wait_for_event_count(
    store: EventStore,
    thread_id: str,
    event_type: str,
    count: int,
    timeout: float = 5.0,
) -> list[Event]:
    """Wait until at least `count` events of `event_type` exist; return them.

    Example:
        # Wait for 2 AGENT_MESSAGE events (initial response + continuation)
        wait_for_event_count(store, agent_thread_id, "AGENT_MESSAGE", 2)
    """
    deadline = time.monotonic() + timeout
    while True:
        matching = [e for e in store.get_events(thread_id) if e.type == event_type]
        if len(matching) >= count:
            return matching
        if time.monotonic() > deadline:
            raise TimeoutError(
                f"Timeout waiting for {count} {event_type} events after "
                f"{timeout}s (got {len(matching)})"
            )
        time.sleep(0.01)


def wait_for_event_match(
    store: EventStore,
    thread_id: str,
    predicate: Callable[[Event], bool],
    description: str,
    timeout: float = 5.0,
) -> Event:
    """Wait for the first event matching `predicate` (checks data, not just type).

    Example:
        wait_for_event_match(
            store, agent_thread_id,
            lambda e: e.type == "TOOL_RESULT" and e.data["id"] == "call_123",
            "TOOL_RESULT with id=call_123",
        )
    """
    deadline = time.monotonic() + timeout
    while True:
        event = next((e for e in store.get_events(thread_id) if predicate(e)), None)
        if event is not None:
            return event
        if time.monotonic() > deadline:
            raise TimeoutError(f"Timeout waiting for {description} after {timeout}s")
        time.sleep(0.01)


# Usage from an actual debugging session:
#
# BEFORE (flaky):
# ---------------
#   agent.send_message("Execute tools")   # runs in a background thread
#   time.sleep(0.3)                        # hope tools start within 300ms
#   agent.abort()
#   time.sleep(0.05)                       # hope results arrive within 50ms
#   assert len(tool_results) == 2          # fails randomly
#
# AFTER (reliable):
# -----------------
#   agent.send_message("Execute tools")
#   wait_for_event_count(store, thread_id, "TOOL_CALL", 2)    # wait for tools to start
#   agent.abort()
#   wait_for_event_count(store, thread_id, "TOOL_RESULT", 2)  # wait for results
#   assert len(tool_results) == 2          # always succeeds
#
# Result: 60% pass rate → 100%, faster execution (no over-long fixed waits).
