import logging.config
from logging import Logger

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters
    "formatters": {
        "std_format": {
            "format": "{levelname}: {asctime} [{name}] | {message} | "
            "File {module}.py, Func {funcName}() on {lineno} line",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "serv_format": {
            "format": "{levelname}: {asctime} [{name}] | {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    # Handlers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "std_format",
        },
        "uvicorn": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "serv_format",
        },
    },
    # Loggers
    "loggers": {
        "uvicorn.access": {"level": "DEBUG", "handlers": ["console"]},
        "Server": {"level": "DEBUG", "handlers": ["uvicorn"]},
        "voting": {"level": "DEBUG", "handlers": ["console"]},
        "utils": {"level": "DEBUG", "handlers": ["console"]},
    },
}

logging.config.dictConfig(logger_config)


def get_logger(name: str) -> Logger:
    logger = logging.getLogger(name)
    return logger
