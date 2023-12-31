#!/bin/bash

BASEPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; cd ..; pwd -P )"
cd $BASEPATH

if [ -f "venv" ];
then
  python3 -m venv venv
fi

. venv/bin/activate
pip install -r requirements.txt

