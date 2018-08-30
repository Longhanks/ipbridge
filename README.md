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

- Python 3.6 or newer
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

- LaunchAgents:
  - asabridge:
    - Change working directory from `/Users/aschulz/Projects/asabridge` to the deployment directory.
    - Change the stdout and stderr paths to the desired log file path.
  - logstream:
    - Change `LOG_FILE_PATH` as above.
- Change the `LOG_FILE_PATH` in `asabridge/logs/views.py` as above.
- Change the `IMAGE_CACHE_PATH` in `asabridge/readinglist/readinglist.py` to an other temporary directory if `/tmp` is unsuitable or not writable.
  - This must be changed in the nginx config, too, to enable serving the cached reading list preview images.
- Use the LaunchAgents to start asabridge and the logstream.
- nginx config:
  - Change the domain name and the path to the SSL certificate + key.
  - If `IMAGE_CACHE_PATH` was changed as mentioned above, change it here, too.
  - Change the path to the static files to the deployment directory.
- Adapt as desired the `gunicorn_config.py`.
  -  Do not increase the number of workers, as it breaks flask-socketio ([see also](https://flask-socketio.readthedocs.io/en/latest/#gunicorn-web-server)).

## Ideas/ToDo

- Tests.
