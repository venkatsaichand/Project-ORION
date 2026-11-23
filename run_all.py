from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from orion_pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(PROJECT_ROOT)
