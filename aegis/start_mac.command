#!/bin/bash
set -e

# Always run from the folder that contains this launcher.
cd "$(dirname "$0")"

echo "========================================"
echo "        A.E.G.I.S. VISION // macOS"
echo "========================================"
echo

# Prefer python3. Fall back to common Homebrew/local locations.
if command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
elif [ -x /usr/local/bin/python3 ]; then
    PYTHON="/usr/local/bin/python3"
elif [ -x /opt/homebrew/bin/python3 ]; then
    PYTHON="/opt/homebrew/bin/python3"
else
    echo "ERROR: Python 3 was not found. Install Python 3 and run this file again."
    read -n 1 -s -r -p "Press any key to close..."
    exit 1
fi

# Create the virtual environment automatically on first launch.
if [ ! -f ".venv/bin/activate" ]; then
    echo "[AEGIS] First launch: creating virtual environment..."
    "$PYTHON" -m venv .venv
fi

source .venv/bin/activate

# Install dependencies only when needed (first launch / requirements changed).
REQ_HASH="$(shasum requirements.txt | awk '{print $1}')"
STAMP_FILE=".venv/.aegis_requirements_hash"
OLD_HASH=""
[ -f "$STAMP_FILE" ] && OLD_HASH="$(cat "$STAMP_FILE")"

if [ "$REQ_HASH" != "$OLD_HASH" ]; then
    echo "[AEGIS] Installing/updating dependencies..."
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo "$REQ_HASH" > "$STAMP_FILE"
fi

echo "[AEGIS] Launching Vision Core..."
echo
python run.py
STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo
    echo "[AEGIS] Application exited with error code $STATUS."
    read -n 1 -s -r -p "Press any key to close..."
fi
