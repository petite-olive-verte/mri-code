import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_VENDOR_DIR = _REPO_ROOT / ".mri-installer-kit"
if str(_VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(_VENDOR_DIR))

VERSION = (_REPO_ROOT / "VERSION").read_text().strip()
PAYLOAD_DIR = _REPO_ROOT / "payload"
