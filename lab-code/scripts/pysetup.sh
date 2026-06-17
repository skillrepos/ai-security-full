#!/usr/bin/env bash
# Sets up the Python environment for the AI Security full-day labs.
PYTHON_ENV=${1:-py_env}
python3 -m venv ./$PYTHON_ENV \
    && export PATH=./$PYTHON_ENV/bin:$PATH \
    && grep -qxF "source $(pwd)/$PYTHON_ENV/bin/activate" ~/.bashrc \
    || echo "source $(pwd)/$PYTHON_ENV/bin/activate" >> ~/.bashrc
source ./$PYTHON_ENV/bin/activate
if [ -f "./requirements.txt" ]; then
    pip3 install -r "./requirements.txt"
fi
echo "Environment ready. Labs are self-contained (stdlib + PyYAML)."
