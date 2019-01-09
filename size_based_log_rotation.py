import time
import os
import zlib
import logging
import logging.handlers
from logging import Formatter

# name the compressed file
def namer(name):
    return name + ".gz"

# read the data from source, compress it, write it to dest and delete source
def rotator(source, dest):
    with open(source, "rb") as sf:
        data = sf.read()
        compressed = zlib.compress(data, 9)
        with open(dest, "wb") as df:
            df.write(compressed)
    os.remove(source)

def create_size_based_rotating_log(log_path):
    """"""

    # Checks if the path exists otherwise tries to create it
    if not os.path.exists(log_path):
        try:
            os.makedirs(log_path)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type, exc_value, exc_traceback)

    # Sets the format and level of logging records
    format = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = Formatter(format)
    level=logging.DEBUG

    # Does basic configuration for the logging system
    logging.basicConfig(format=format, level=level)

    # Instantiates a logger object
    logger = logging.getLogger("Rotating Log")
 
    # Creates at most 5 backup whenever the filesize equals to or exceeds 250 bytes
    handler = logging.handlers.RotatingFileHandler(filename=log_path+'tmp.log',
                                       maxBytes=250,
                                       backupCount=5)
    handler.setFormatter(formatter)
    handler.rotator = rotator
    handler.namer = namer
    logger.addHandler(handler)
 
    for i in range(10000):
        logger.debug('%d' % i)
        time.sleep(5)

#----------------------------------------------------------------------

if __name__ == "__main__":
    log_path = "logs/"
    create_size_based_rotating_log(log_path)
