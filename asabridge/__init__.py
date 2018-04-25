#!/usr/bin/env python3

from __future__ import print_function

import sys

major = sys.version_info[0]
minor = sys.version_info[1]
if major < 3 or (major and minor < 3):
    print('Requires Python >= 3.4.')
    sys.exit(1)

# system imports.
from pathlib import Path

if __name__ == '__main__':
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# asabridge imports.
from asabridge.app import app, ssl_context
from asabridge.views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12137, debug=False, ssl_context=ssl_context)
