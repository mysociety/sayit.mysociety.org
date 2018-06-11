set -e
cd "$(dirname "$0")/.."

if [ -z "$VIRTUAL_ENV" ]; then
    VENV=vendor/virtualenv
    if [ -e "$VENV/bin/activate" ]; then
        echo "Using virtualenv in $VENV"
        source $VENV/bin/activate
    else
        echo "No virtualenv detected, creating in $VENV"
        virtualenv $VENV
        source $VENV/bin/activate
        pip install --requirement requirements.txt
    fi
fi
