""" Lambtastic server runner """

import os
from bottle import run, default_app
from core import app as core_app
import settings

if __name__ == "__main__":
    run(
        default_app(),
        host='localhost',
        port=8080,
        debug=settings.BOTTLE_DEBUG is True,
        reloader=settings.BOTTLE_AUTORELOAD is True
    )
else:
    os.chdir(os.path.dirname(__file__))
    application = default_app()