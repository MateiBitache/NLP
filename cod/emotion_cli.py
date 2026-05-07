from pathlib import Path
import sys


# Keep this wrapper tiny: it lets the project run without installing the package.
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emotion_analysis.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
