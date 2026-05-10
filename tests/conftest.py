import sys
import os

# Add the project root to PYTHONPATH so `from src.X import ...` works in tests.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Also add src/ so internal imports like `from category_rules import ...` still work at runtime.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

