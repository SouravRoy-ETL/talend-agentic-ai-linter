import subprocess
import sys
from src.main import lint_and_fix_all_jobs

# ✅ Run syntax validator first
print("🔍 Validating YAML rule syntax...")
validate = subprocess.run(['python', 'validate_syntax.py'], capture_output=True, text=True)
if validate.returncode != 0:
    print("❌ YAML validation failed:")
    print(validate.stdout)
    print(validate.stderr)
    sys.exit(1)

# 🧰 Extract .item jobs from zipped_jobs folder
print("🧰 Extracting .item files from zipped_jobs...")
extract_result = subprocess.run(['python', 'extract_items_from_job.py'])
if extract_result.returncode != 0:
    print("❌ Failed to extract jobs.")
    sys.exit(1)

# 🚀 Launch main linting and fixing process
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()
    lint_and_fix_all_jobs(verbose=args.verbose)
