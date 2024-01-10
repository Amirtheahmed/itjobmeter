import logging

class CustomFormatter(logging.Formatter):
    """Custom logging Formatter with color codes."""

    FORMATS = {
        logging.DEBUG: "\033[94mDEBUG - %(asctime)s - %(message)s\033[0m",
        logging.INFO: "\033[92mINFO - %(asctime)s - %(message)s\033[0m",
        logging.WARNING: "\033[93mWARNING - %(asctime)s - %(message)s\033[0m",
        logging.ERROR: "\033[91mERROR - %(asctime)s - %(message)s\033[0m",
        logging.CRITICAL: "\033[95mCRITICAL - %(asctime)s - %(message)s\033[0m"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(name=__name__, level=logging.DEBUG):
    # Check if the logger has handlers already configured
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)

        # Create handlers
        c_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        c_handler.setFormatter(CustomFormatter())

        # Add handlers to the logger
        logger.addHandler(c_handler)

    return logger

