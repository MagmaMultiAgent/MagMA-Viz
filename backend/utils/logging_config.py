import logging
import sys

def configure_logging():
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
