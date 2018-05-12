# asabridge

Web access to local macOS services.

## Requirements

- Python 3.4 or newer
- [cliclick](https://www.bluem.net/de/projekte/cliclick/ "cliclick")
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

### Dev

```bash
FLASK_APP=autoapp.py FLASK_ENV=development flask run
```

### Production

- LaunchAgents: Change working directory from /Users/aschulz/Projects/asabridge to somwhere else.
- Use the LaunchAgents to start asabridge at port 12136 and a log tailer that pipes to rtail.
- nginx conf: Add domain name and SSL certificate + key. Provides a reverse proxy from 12137 to asabridge.
- Take a look at the LaunchAgent plist to see the gunicorn flags.
- Run [rtail-server](https://github.com/Longhanks/rtail-server "rtail-server") at 12138 (reverse proxy 12139).

## Ideas/ToDo

- Implement index/landing page.
- Move /logs out of login to an own submodule.
- Implement caching + auto syncback.
