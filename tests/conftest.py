import sys
import pathlib

# Ensure the repository root is on sys.path for pytest runs so local modules import cleanly
repo_root = pathlib.Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
