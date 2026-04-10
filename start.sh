#!/bin/env bash

export PYTHONPATH=/run/media/aruncs/WORK/ApiTesting:$PYTHONPATH
source .venv/bin/activate

pytest -xm auth -v
