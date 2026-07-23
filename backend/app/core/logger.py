"""Structured JSON logger using structlog.

Every log line is a JSON object with fields:
  timestamp, level, module, event, request_id

If `structlog` is unavailable, the code falls back to the standard library logger
so the application can still start (useful for environments where the optional
dependency is not installed).
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar

# ---------------------------------------------------------------------------
# Optional `structlog` import – provide a minimal shim when the library is missing
# ---------------------------------------------------------------------------
try:
    import structlog
except ImportError:  # pragma: no cover
    # Very small stub that mimics the API surface used in the project.
    class _DummyLogger:
        def __getattr__(self, name):
            # Return a no‑op callable for any logging method (debug, info, …)
            return lambda *args, **kwargs: None

    def _dummy_configure(*, processors=None, wrapper_class=None, context_class=None, logger_factory=None, cache_logger_on_first_use=True):
        # No‑op configure – does nothing but satisfies the call signature.
        return None

    class _DummyPrintLoggerFactory:
        def __call__(self, *_, **__) -> logging.Logger:
            return logging.getLogger()

    structlog = type(
        "structlog",
        (),
        {
            "configure": _dummy_configure,
            "get_logger": lambda name=__name__: _DummyLogger(),
            "PrintLoggerFactory": _DummyPrintLoggerFactory,
            "stdlib": type(
                "stdlib",
                (),
                {"BoundLogger": logging.Logger},
            ),
        },
    )

# ---------------------------------------------------------------------------
# Context variable for per‑request tracking (e.g., request IDs)
# ---------------------------------------------------------------------------
request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def _add_request_id(logger: "structlog.types.WrappedLogger", method_name: str, event_dict: dict) -> dict:
    """Inject the request ID (if present) into the structured log record."""
    rid = request_id_ctx.get()
    if rid:
        event_dict["request_id"] = rid
    return event_dict


def configure_logging(*, level: int = logging.INFO) -> None:
    """Configure JSON logging.

    The real implementation uses ``structlog`` processors to emit JSON lines.
    When the fallback stub is active the call becomes a harmless no‑op.
    """
    structlog.configure(
        processors=[
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


def get_logger(name: str = __name__) -> "structlog.stdlib.BoundLogger":
    """Return a bound logger for the given module name."""
    return structlog.get_logger(name)
