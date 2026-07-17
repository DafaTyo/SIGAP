"""Re-export settings for convenience.

Usage in router:
    from app.dependencies import settings
"""

from app.core.config import settings

__all__ = ["settings"]
