import logging
import os

# Create reports/logs folder if it doesn't exist
LOG_DIR = os.path.join("reports", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "errors.log")
log_format_string = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

def get_logger(name: str = __name__) -> logging.Logger:
    """Creates a logger that logs INFO+ to console and WARNING+ to file. write to pytest.ini"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  

    if not logger.handlers:
        # write to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter(log_format_string,datefmt="%Y-%m-%d %H:%M:%S")
        ch.setFormatter(ch_formatter)
        logger.addHandler(ch)
        # write to file
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.WARNING)
        fh_formatter = logging.Formatter(log_format_string,datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(fh_formatter)
        logger.addHandler(fh)

    return logger
