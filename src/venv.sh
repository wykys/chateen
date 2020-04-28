#!/usr/bin/env bash
# create and install python enviroment
# wykys 2018


if [ -d ".venv" ]; then
    echo "remove old venv"
    rm .venv -rf
fi

echo "create new venv"
python3.8 -m venv .venv

echo "activate venv"
. .venv/bin/activate

echo "upgrade pip"
pip install --upgrade pip

echo "install modules from requirements"
pip install -r ../requirements.txt

echo "installed modules"
pip freeze