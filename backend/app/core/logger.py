"""Structured JSON logger using structlog.

Every log line is a JSON object with fields:
  timestamp, level, module, event, request_id

References:
  - AGENTS.md: "Audit Logging" requirement
  - core/TASK.md: "Add logger utility — JSON log format"
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar

import structlog

# Context variable for per-request tracking
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def _add_request_id(
    logger: structlog.types.WrappedLogger,
    method_name: str,
    event_dict: dict,
) -> dict:
    rid = request_id_ctx.get()
    if rid:
        event_dict["request_id"] = rid
    return event_dict


def configure_logging(*, level: int = logging.INFO) -> None:
    """Call once at app startup to wire structlog → stdlib JSON."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            _add_request_id,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = __name__) -> structlog.stdlib.BoundLogger:
    """Return a bound logger with the given module name."""
    return structlog.get_logger(name)
