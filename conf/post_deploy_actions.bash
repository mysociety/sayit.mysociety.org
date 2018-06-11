#!/bin/bash

# abort on any errors
set -e

# check that we are in the expected directory
cd `dirname $0`/..

# create/update the virtual environment
# --system-site-packages is present so we can use python-opencv with ease.
virtualenv_args="--system-site-packages"
virtualenv_dir='../virtualenv-sayit'
virtualenv_activate="$virtualenv_dir/bin/activate"
if [ ! -f "$virtualenv_activate" ]
then
    virtualenv $virtualenv_args $virtualenv_dir
fi
source $virtualenv_activate

# Upgrade pip to a secure version
pip_version="$(pip --version)"
if [ "$(echo -e 'pip 1.4\n'"$pip_version" | sort -V | head -1)" = "$pip_version" ]; then
    curl -L -s https://bootstrap.pypa.io/get-pip.py | python
fi

# cryptography's install finds the system setuptools, which finds the
# system six, which is too old. To avoid this, update setuptools in the
# virtualenv.
pip install -U setuptools

script/update --deployment
