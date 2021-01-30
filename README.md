# Government Identity Verification Engine

## Transaction Logging Service

The Transaction Logging Service is a component of GIVE that provides logging for Verification Events.

## Pre-requisites
- [Python 3.9](https://www.python.org/)
- [CloudFoundry CLI](https://docs.cloudfoundry.org/cf-cli/)

## Building Locally

Run this script to download the code and set up the development environment with python virtual env. The pre-commit hook provides code formatting using [black](https://black.readthedocs.io/en/stable/)

```
git clone https://github.com/18F/identity-give-transaction-logging
cd identity-give-transaction-logging
python3 -m venv .venv
source .venv/bin/activate
# .venv\Scripts\Activate.ps1 on Windows
python3 -m pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
```

Run the application with:

```
python manage.py migrate
python manage.py collectstatic
gunicorn -b 127.0.0.1:8080 transaction_log.wsgi
```

A windows alternative for gunicorn is `waitress`:

``` 
pip install waitress

waitress-serve --port=8080 transaction_log.wsgi:application
```


### Available Endpoints

`/transaction`
