# asabridge

Web access to local macOS services.

## Requirements

- Python 3.4 or newer
- [cliclick](https://www.bluem.net/de/projekte/cliclick/ "cliclick")
- [redis](https://redis.io "redis")

## Getting started

```bash
virtualenv venv
. venv/bin/activate
pip install -e .
```

You must find a way to allow the processes nginx, gunicorn and python3 to control your computer (macOS Security settings).
For example, use [tccutil](https://github.com/jacobsalmela/tccutil "tccutil").

## Running

### Dev

```bash
FLASK_APP=autoapp.py FLASK_ENV=development flask run
```

### Production

Use the nginx config file for a reverse proxy. Take a look at the LaunchAgent plist to see the gunicorn flags. Then start gunicorn and nginx to deploy the application.

## Ideas/ToDo

- Implement caching + auto syncback.
- Implement proper login via session.
