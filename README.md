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

You will need to have the following installed:

* [elasticsearch](http://elasticsearch.org/)

* PostgreSQL

* The compass and zurb-foundation gems. Something like the following should
  install them, with the relevant gem bin directory then added to your `PATH`:

        gem install --user-install --no-document zurb-foundation compass

* pip, virtualenv and yui-compressor.

* The development files for libffi and libssl
  (if you're installing on a Mac, you might want to look at
  https://cryptography.io/en/latest/installation/)

There is a list of the required Debian/Ubuntu packages in conf/packages.

Clone the repository:

    mkdir sayit.mysociety.org
    cd sayit.mysociety.org
    git clone https://github.com/mysociety/sayit.mysociety.org

Create a PostgreSQL database and user:

    sudo -u postgres psql
    postgres=# CREATE USER sayit WITH password 'sayit';
    CREATE ROLE
    postgres=# CREATE DATABASE sayit WITH OWNER sayit;
    CREATE DATABASE

Set up a python virtual environment, activate it, and install the required
python packages:

    virtualenv virtualenv-sayit
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
