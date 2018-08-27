# asabridge

Web access to local macOS services.

## Requirements

- Python 3.4 or newer
- [redis](https://redis.io "redis")

## Installation

```bash
virtualenv venv
. venv/bin/activate
pip install -e .
```

You must find a way to allow the processes nginx, gunicorn and python3 to control your computer (macOS Security settings).
For example, use [tccutil](https://github.com/jacobsalmela/tccutil "tccutil").

## Running

### Development

```bash
FLASK_APP=autoapp.py FLASK_ENV=development python3 -m flask run
```

### Production

- LaunchAgent: Change working directory from /Users/aschulz/Projects/asabridge to somwhere else.
- Also change the `LOG_FILE_PATH` in `asabridge/logs/views.py` to fit what's in the LaunchAgent as stdout file path.
- Use the LaunchAgent to start asabridge at port 12136.
- nginx conf: Add domain name and SSL certificate + key. Provides a reverse proxy from 12137 to asabridge.
- Take a look at the LaunchAgent plist to see the gunicorn flags.

## Ideas/ToDo

- Tests.
