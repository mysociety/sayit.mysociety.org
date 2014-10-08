#!/bin/bash

# abort on any errors
set -e

# check that we are in the expected directory
cd `dirname $0`/..

# create/update the virtual environment
# --system-site-packages is present so we can use python-opencv with ease.
virtualenv --system-site-packages ../virtualenv-sayit
source ../virtualenv-sayit/bin/activate
pip install --requirement requirements.txt

# make sure that there is no old code (the .py files may have been git deleted)
find . -name '*.pyc' -delete

# get the database up to speed
./manage.py syncdb
./manage.py migrate

# Install gems in order to compile the CSS
bundle install --deployment --path ../gems --binstubs ../gem-bin

# gather all the static files in one place
./manage.py collectstatic --noinput
