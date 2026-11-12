
#!/usr/bin/env bash
set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: ./run.sh <input_dir> <output.json>"
    exit 1
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Error: Python is not installed."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

"$PYTHON" "$SCRIPT_DIR/solution.py" "$1" "$2"
