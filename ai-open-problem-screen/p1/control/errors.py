"""Shared exception types."""


class ControlError(RuntimeError):
    """Base class for orchestration failures."""


class ValidationError(ControlError):
    """Raised when an artifact fails a fail-closed validation."""


class LockError(ControlError):
    """Raised when exclusive state ownership cannot be established."""


class TransitionError(ControlError):
    """Raised for an unauthorized or invalid campaign-state transition."""
