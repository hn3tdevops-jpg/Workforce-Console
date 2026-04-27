import sys
from pathlib import Path
proj = str(Path(__file__).parent)
if proj not in sys.path:
    sys.path.insert(0, proj)
from app import app as application
