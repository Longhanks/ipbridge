# system imports.

from pathlib import Path

# flask imports.
from flask import Flask
from flask_httpauth import HTTPBasicAuth

# Create SSL context.
ssl_context = None
certs = Path(__file__).resolve().parent / 'certs'
if certs.exists() and certs.is_dir():
    ssl_context = (str(certs / 'fullchain.pem'), str(certs / 'privkey.pem'))

app = Flask(__name__)
auth = HTTPBasicAuth()
