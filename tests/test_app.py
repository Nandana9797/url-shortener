import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.app import app


def test_app_exists():
    assert app is not None
