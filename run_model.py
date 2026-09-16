"""Repository-local entry point.

Run ``python run_model.py --all-scenarios`` from the project root without
requiring an editable installation first.
"""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from north_co2_model.cli import main  # noqa: E402


if __name__ == "__main__":
    main()

