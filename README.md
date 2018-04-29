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

## Running

### Dev

```bash
FLASK_APP=asabridge FLASK_DEBUG=1 flask run
```

### Production

Needs `asabridge/certs/fullchain.pem` and `asabridge/certs/privkey.pem`.

```bash
python3 asabridge/__init__.py
```

## Ideas/ToDo

- Implement caching + auto syncback.
- Implement proper login via session.
