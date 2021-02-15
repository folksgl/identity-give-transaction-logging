![Tests](https://github.com/18F/identity-give-transaction-logging/workflows/Unit-Tests/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/f9b10f2d60f8e8baef84/maintainability)](https://codeclimate.com/github/18F/identity-give-transaction-logging/maintainability)
![Black](https://github.com/18F/identity-give-transaction-logging/workflows/Black/badge.svg)

# Government Identity Verification Engine

## Transaction Logging Service

The Transaction Logging Service is a component of GIVE that provides logging for Verification Events.

## Building Locally

### Pre-requisites
Make sure you have the following installed if you intend to build the project locally.
- [Python 3.9](https://www.python.org/)
- [CloudFoundry CLI](https://docs.cloudfoundry.org/cf-cli/)

### Development setup
To set up your environment, run the following commands (or the equivalent commands if not using a bash-like terminal):
```shell
# Clone the project
git clone https://github.com/18F/identity-give-transaction-logging
cd identity-give-transaction-logging
# Set up Python virtual environment
python3.9 -m venv .venv
source .venv/bin/activate
# .venv\Scripts\Activate.ps1 on Windows
# Install dependencies and pre-commit hooks
python -m pip install -r requirements-dev.txt
pre-commit install
```

:warning: **If you are not able to install `psycopg2`**, please make sure you have `libpq-dev` installed on your system. For apt, use the following `sudo apt install -y libpq-dev`

### Required environment variables
The Django settings.py file for this project requires setting an environment variable: `SECRET_KEY`
Running the following in your shell should print a secret key that can be used.
```shell
python
import secrets
secrets.token_urlsafe()
exit()

```

Set the environment variable using *the entire output* (including quotes) from the printed secret
```shell
# BASH-like shells
export SECRET_KEY=<your-secret-here>
```
```powershell
# PowerShell
Env:SECRET_KEY=<your-secret-here>
```
Note: during development, it may also be helpful to add the `DEBUG` environment variable and setting it to the string `True`

### Running the application
After completing [development setup](#development-setup) and [environment variable setup](#required-environment-variables) you can run the application with:

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
