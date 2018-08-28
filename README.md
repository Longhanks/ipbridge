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
  - Live stream of new log lines via [SSE](https://en.wikipedia.org/wiki/Server-sent_events "Server-sent events")

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

- LaunchAgent: Change working directory from `/Users/aschulz/Projects/asabridge` to the deployment directory.
- Change the `LOG_FILE_PATH` in `asabridge/logs/views.py` to fit what's in the LaunchAgent as stdout file path.
- Change the `IMAGE_CACHE_PATH` in `asabridge/readinglist/readinglist.py` to an other temporary directory if `/tmp` is unsuitable or not writable.
  - This must be changed in the nginx config, too, to enable serving the cached reading list preview images.
- Use the LaunchAgent to start asabridge at port 12136.
- nginx config: Add the domain name, the SSL certificate and key. This configuration provides a reverse proxy from 12137 to asabridge.
- Take a look at the LaunchAgent plist to see the gunicorn flags.

## Ideas/ToDo

- Tests.
