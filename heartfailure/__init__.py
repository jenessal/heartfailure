import os
from flask import Flask

app = Flask(__name__)
app.config.from_object('heartfailure.default_settings')
app.config.from_envvar('HEARTFAILURE_SETTINGS')

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(app.config['LOG_DIR'], 'heartfailure.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

import heartfailure.views
