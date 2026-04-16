# services/__init__.py

# IMPORTS LAZY (NO ROMPEN PYTEST)
from .ml_service import predict
from .classify_service import classify_text
from .narrate_service import narrate

__all__ = ["predict", "classify_text", "narrate"]