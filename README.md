[![CircleCI](https://circleci.com/gh/18F/identity-give-transaction-logging.svg?style=shield)](https://circleci.com/gh/18F/identity-give-transaction-logging)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Government Identity Verification Engine

## Transaction Logging Service

The Transaction Logging Service is a component of GIVE that provides logging for Verification Events.

## Pre-requisites
- [Python 3.9](https://www.python.org/)
- [CloudFoundry CLI](https://docs.cloudfoundry.org/cf-cli/)

## Building Locally

Run this script to download the code and set up the development environment with python virtual env. The pre-commit hook provides code formatting using [Black](https://black.readthedocs.io/en/stable/)

```shell
git clone https://github.com/18F/identity-give-transaction-logging
cd identity-give-transaction-logging
python3.9 -m venv .venv
source .venv/bin/activate
# .venv\Scripts\Activate.ps1 on Windows
python -m pip install -r requirements-dev.txt
pre-commit install
```

Run the application with:

```shell
python manage.py migrate
python manage.py collectstatic
gunicorn -b 127.0.0.1:8080 transaction_log.wsgi
```

A windows alternative for gunicorn is `waitress`:

``` shell
pip install waitress

waitress-serve --port=8080 transaction_log.wsgi:application
```


### Available Endpoints

`/transaction`
