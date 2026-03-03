# app/logger.py
import logging

# simple helper so the file exists (optional to use)
def get_logger(name: str = "calculator") -> logging.Logger:
    return logging.getLogger(name)