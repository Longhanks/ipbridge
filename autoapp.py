# -*- coding: utf-8 -*-
import eventlet

eventlet.monkey_patch()

from asabridge.app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
