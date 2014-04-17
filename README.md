sayit.mysociety.org
===================

A Django project using [SayIt](https://github.com/mysociety/sayit) to store
transcripts and present them in a modern, searchable format.

Examples of SayIt in action:

* [The Leveson Inquiry](http://leveson.sayit.mysociety.org/)
* [The Charles Taylor trial](http://charles-taylor.sayit.mysociety.org/)
* [The plays of Shakespeare](http://shakespeare.sayit.mysociety.org/)

SayIt is a [Poplus component](http://poplus.org/)
by [mySociety](http://www.mysociety.org/)

Installation
------------

You'll need to have pip, virtualenv and yui-compressor (Debian/Ubuntu
packages python-pip, python-virtualenv and yui-compressor).

Clone the repository:

    mkdir sayit.mysociety.org
    cd sayit.mysociety.org
    git clone https://github.com/mysociety/sayit.mysociety.org

Create a postgres database and user:

    sudo -u postgres psql
    postgres=# CREATE USER sayit WITH password 'sayit';
    CREATE ROLE
    postgres=# CREATE DATABASE sayit WITH OWNER sayit;
    CREATE DATABASE

Set up a python virtual environment, activate it, and install the required
python packages:

    virtualenv --no-site-packages virtualenv-sayit
    source virtualenv-sayit/bin/activate
    cd sayit.mysociety.org
    pip install --requirement requirements.txt

Alter the settings to match your setup:

    cp conf/general.yml-example conf/general.yml

Set up the database:

    ./manage.py syncdb
    ./manage.py migrate

The development server should now run fine:

    ./manage.py runserver

You'll want to use http://127.0.0.1.xip.io:8000/ and instances can be seen at
e.g. http://default.127.0.0.1.xip.io:8000/

To gather all the static files together in deployment, you'll use:

    ./manage.py collectstatic --noinput
