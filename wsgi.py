import sys
import logging
logging.basicConfig(stream=sys.stderr)

from app import portfolio as application
portfolio = application