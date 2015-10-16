#!/usr/bin/env python

import sys
if sys.version_info < (3, 0):
    sys.stderr.write("Sorry, requires Python 3.4 or later\n")
    sys.exit(1)

import os
import logging

from Util.utils import app_logger, project_file
from flask import Flask
from Services.Blueprints import indexPrint
from gludb.config import Database, default_database

from config import env_populate


# Note that application as the main WSGI app is required for Python apps
# on Elastic Beanstalk. Also note that we provide the default config, but
# someone must supply an actual config file pointed to by the env variable
# GLUTEN_CONFIG_FILE. See ./local.sh for an example of how to handle this
application = Flask(__name__)
application.config.from_object('config.DefaultConfig')
application.config.from_envvar('GLUTEN_CONFIG_FILE')
application.secret_key = application.config.get('FLASK_SECRET')

# Set any environment var's requested by the config file
for name in env_populate:
    os.environ[name] = application.config.get(name)

# Final app settings depending on whether or not we are set for debug mode
# Note that once we get everything working, we'll have be able to use the
# logging help in gluten.utils (like app_logger)
if application.config.get('DEBUG', None):
    # Debug mode - running on a workstation
    application.debug = True
    logging.basicConfig(level=logging.DEBUG)
else:
    # We are running on AWS Elastic Beanstalk (or something like it)
    application.debug = False
    # See .ebextensions/01logging.config
    logging.basicConfig(
        filename='/opt/python/log/gluten.log',
        level=logging.INFO
    )

app_logger().info('Application debug is %s', application.debug)

# Register our blueprints
application.register_blueprint(indexPrint)
#application.register_blueprint(main)
#application.register_blueprint(admin)


# This will be called before the first request is ever serviced
@application.before_first_request
def before_first():
    app_logger().info('Handling database init')

    if application.debug:
        # Debug/local dev
        default_database(Database('sqlite', filename=project_file('.test.db')))
    else:
        # Production!
        default_database(Database('dynamodb'))

    # Make sure we have our tables
    #User.ensure_table()
    #Transcript.ensure_table()
    #Taxonomy.ensure_table()



# Our entry point - called when our application is started "locally".
# This WILL NOT be run by Elastic Beanstalk
def main():
    # Listen on all addresses if running under Vagrant, else listen
    # on localhost
    host = '0.0.0.0' if os.environ['USER'] == 'vagrant' else '127.0.0.1'
    application.run(host=host)
if __name__ == '__main__':
    main()
