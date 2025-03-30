import logging

# Configure logging settings
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message):
    """Logs an informational message."""
    logging.info(message)

def log_error(message):
    """Logs an error message."""
    logging.error(message)
