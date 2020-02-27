#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/CBC/")

from CBC import app as application
application.secret_key = 'IFITMASH'
