"""Fail-closed orchestration controls for the LR-positivity campaign.

The package deliberately depends only on the Python standard library.  It does
not evaluate LR coefficients and it never advances the scientific campaign on
its own; it validates evidence and supplies transactional control primitives.
"""

from .errors import ControlError, ValidationError

__all__ = ["ControlError", "ValidationError"]
__version__ = "1.0.0"
