#!/bin/bash

cd laidebug_engine/laidebug_engine
python -m venv .
source bin/activate
pip install -r requirements.txt
deactivate

cd ../../laidebug_api
python -m venv .
source bin/activate
pip install -r requirements.txt
deactivate
