#!/usr/bin/env bash
# run chateen
# wykys 2020

SCRIPTS_DIR=.scripts

if [ ! -d ".venv" ]; then
    ./venv.sh
fi

. .venv/bin/activate
export QT_QPA_PLATFORMTHEME=gtk3
pyside2-uic gui/chateen.ui -o gui/main_window_template.py
./chateen.py
