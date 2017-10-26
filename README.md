# Flask sample app using blueprints

This is an easy example app with focus on its modularity and its purpose is
purely a helping reference when working with blueprints for avoiding circular
imports and such.

App is divided into two blueprints, site and api. They both use the same
database context defined in `config/base.py` settings file, along with other
settings variables which can be defined in separate `.env` file.
Other variables can be easily added in the same manner.
That way, settings are easily adjustable for both develompment and
production purposes.

Tests use their settings, hardcoded inside `config/test.py`.
`Tests.py` defines a location for the test loader to search for tests, as well
as settings for coverage.

To work with the database directly from the python shell, import db to setup
app context first:

    from run import db

After that, models will know in which context they belong and can be imported
and used:

    from app.models import User

## Quick start

Get the source code:

    git@github.com:HBalija/flask-blueprints.git

Navigate to flask-blue folder:

    cd flask-blueprints

Create a `python3` virtual environment:

    mkvirtualenv --python=/usr/bin/python3 flask-blueprints

Install requirements:

    pip install -r requirements.txt

Create `.env` file and set variales as shown in env,sample.

## Running app

To start develoment server, run:

    ./run.py

Navigate to:

    127.0.0.1:5000

## Running tests

To run tests, run:

    ./tests.py
