# asabridge

Web access to local macOS services. Current features:

- Authentication system via system credentials
  - Login/logout via PAM to securely authenticate access
  - Save login via cookie
  - Redirect to previously entered URL once authenticated
- Access to the Safari Reading List
  - See saved links, preview images and date added
  - Remove elements
  - Add new URLs
  - Instant response using [redis](https://redis.io "redis") cache
- Access to the application's log file
  - Previously logged lines
  - Live stream of new log lines via [socket.io](https://socket.io "socket.io")

## Requirements

- [pipenv](https://pipenv.readthedocs.io/en/latest/ "pipenv")
- [redis](https://redis.io "redis")

## Installation

```bash
pipenv install
```

Granting assistive access via System Preferences is required for these processes:
- ```/usr/local/Cellar/python/3.7.0/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Contents/MacOS/Python```
- ```/usr/local/bin/gunicorn```

## Running

### Development

```bash
FLASK_APP=asabridge_app.py FLASK_ENV=development python3 -m flask run
```

### Production

- LaunchAgent:
  - Change working directory from `/Users/aschulz/Projects/asabridge` to the deployment directory.
  - Change the stdout and stderr paths to the desired log file path.
- Use the LaunchAgent to start asabridge.
- nginx config:
  - Change the domain name and the path to the SSL certificate + key.
  - `IMAGE_CACHE_PATH` must be a directory where asabridge can cache temporary images.
  - Change the path to the static files and the favicons to the deployment directory.
- `asabridge/config.py` (`ProductionConfig`):
  - Change the `IMAGE_CACHE_PATH` if it was changed in the nginx configration.
  - Change `SERVER_NAME` to your the same as in the nginx configuration.
  - Generate a new `SECRET_KEY` via `python -c 'import os; print(os.urandom(16))'`.
  - Change `LOG_FILE_PATH` to the stdout path of the LaunchAgent.
  - Do not increase the number of workers, as it breaks flask-socketio ([see also](https://flask-socketio.readthedocs.io/en/latest/#gunicorn-web-server)).

## Ideas/ToDo

- REST API
- SPA front end building upon REST API
- Tests

## Acknowledgements

- favicon:
  - [Feather](https://feathericons.com "feathericons.com") ([MIT License](https://github.com/feathericons/feather/blob/master/LICENSE "MIT License"))
