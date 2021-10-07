#!/bin/sh
SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR
source venv/bin/activate
export PYTHONPATH=$SCRIPT_DIR
python3 ./lite_bot.py
