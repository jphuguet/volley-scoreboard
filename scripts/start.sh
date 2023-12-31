#!/bin/bash

BASEPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; cd ..; pwd -P )"
cd $BASEPATH

. venv/bin/activate
python3 main.py --debug-off

