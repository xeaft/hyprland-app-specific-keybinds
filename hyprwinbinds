#!/bin/sh

if command -v python3 >/dev/null 2>&1; then
    interp="python3"
elif command -v python >/dev/null 2>&1; then
    interp="python"
else
    echo "python interpreter not found" >&2
    exit 1
fi

"$interp" pysrc/main.py "$@"
