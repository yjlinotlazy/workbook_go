"""Allow running chinese_chars as a module: python -m chinese_chars."""

import sys
from pathlib import Path

# Ensure project root is in path so root-level cli.py can be imported
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

import cli  # Top-level module moved to project root

if __name__ == "__main__":
    cli.main()
