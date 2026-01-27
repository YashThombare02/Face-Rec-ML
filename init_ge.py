from great_expectations.data_context import FileDataContext
from pathlib import Path

project_root = Path(".").resolve()

# Create context directory if it doesn't exist
context = FileDataContext.create_context(project_root)

print("✅ Great Expectations initialized successfully!")
