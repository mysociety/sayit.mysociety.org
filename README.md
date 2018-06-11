sayit.mysociety.org
===================

This repository contains a Django project that uses the
[SayIt](https://github.com/mysociety/sayit) component to provide a hosting
service for transcripts, presenting them in a modern, searchable format.

Examples of transcripts hosted by mySociety's deployment of this hosting
project:

* [The Leveson Inquiry](https://leveson.sayit.mysociety.org/)
* [The Charles Taylor trial](https://charles-taylor.sayit.mysociety.org/)
* [The plays of Shakespeare](https://shakespeare.sayit.mysociety.org/)

SayIt is a [Poplus component](http://poplus.org/) by
[mySociety](https://www.mysociety.org/). It is a Django application that can be
included in your own Django project, or run standalone. If you want to host
your own transcripts in SayIt, please see the
[Sayit repository](https://github.com/mysociety/sayit); this repository is a
remote hosting service on top of SayIt, similar to wordpress.com compared with
wordpress.org.

Installation
------------

You will need to have the following installed:

* [elasticsearch](http://elasticsearch.org/) (version 5 is not yet supported)

* PostgreSQL

* bundler, pip, virtualenv and yui-compressor

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

You can run the bootstrap script directly, it will set up a virtualenv for you,
or set up/activate your own virtualenv first if you prefer:

    script/bootstraop

Alter the settings to match your setup:

    cp conf/general.yml-example conf/general.yml

Set up the database, static files and language .mo files:

    script/update

The development server should now run fine:

    script/server

You'll want to use http://127.0.0.1.xip.io:8000/ and instances can be seen at
e.g. http://default.127.0.0.1.xip.io:8000/
