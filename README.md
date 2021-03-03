![Tests](https://github.com/18F/identity-give-transaction-logging/workflows/Unit-Tests/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/f9b10f2d60f8e8baef84/maintainability)](https://codeclimate.com/github/18F/identity-give-transaction-logging/maintainability)
![Black](https://github.com/18F/identity-give-transaction-logging/workflows/Black/badge.svg)

# Government Identity Verification Engine

## Transaction Logging Service

The Transaction Logging Service is a component of GIVE that provides logging
for Verification Events.

## CI/CD Workflows with GitHub Actions
The most up-to-date information about the CI/CD flows for this repo can be
found in the [GitHub workflows directory](https://github.com/18F/identity-give-transaction-logging/tree/main/.github/workflows)

## Building Locally

### Pre-requisites
Make sure you have the following installed if you intend to build the
project locally.
- [Python 3.9](https://www.python.org/)
- [CloudFoundry CLI](https://docs.cloudfoundry.org/cf-cli/)

### Development setup
To set up your environment, run the following commands (or the equivalent
commands if not using a bash-like terminal):
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

:warning: **If you are not able to install `psycopg2`**, please make sure you
have `libpq-dev` installed on your system. For apt, use the following
`sudo apt install -y libpq-dev`

### Required environment variables
The Django settings.py file for this project requires setting an environment
variable: `SECRET_KEY`

Running the following in your shell should print a secret key that can be used.
```shell
python
import secrets
secrets.token_urlsafe()
exit()

```

Set the environment variable using *the entire output* (including quotes) from
the printed secret
```shell
# BASH-like shells
export SECRET_KEY=<your-secret-here>
```
```powershell
# PowerShell
Env:SECRET_KEY=<your-secret-here>
```
Note: during development, it may also be helpful to add the `DEBUG` environment
variable and setting it to the string `True`

### Running the application
After completing [development setup](#development-setup) and
[environment variable setup](#required-environment-variables) you can run the
application with:

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

### Deploying to Cloud.gov during development
All deployments require having the correct Cloud.gov credentials in place. If
you haven't already, visit [Cloud.gov](https://cloud.gov) and set up your
account and CLI.

*manifest.yml* file contains the deployment configuration for cloud.gov, and
expects a vars.yaml file that includes runtime variables referenced. For info,
see [cloud foundry manifest files reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html)

The application database must be deployed prior to the application, and can be
deployed with the following commands:
```shell
cf create-service aws-rds <plan> transaction-log-db
```

*You must wait* until the database has completed provisioning to continue with
the deployment. Wait for the `status` field of `cf service transaction-log-db`
to change from `create in progress` to `create succeeded`.
```shell
watch -n 15 cf service transaction-log-db
```

After the database has come up, running
`cf push --vars-file vars.yaml --var SECRET_KEY=$SECRET_KEY`.

### Available Endpoints

`/transaction`
