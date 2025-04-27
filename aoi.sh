#!/bin/bash

DIR="$(dirname "$(readlink -f "$0")")"

cd "$DIR"
python3 "main.py" "$1"
