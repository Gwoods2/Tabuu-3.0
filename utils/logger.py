import logging
from logging.handlers import TimedRotatingFileHandler


def create_logger() -> None:
    """Creates a basic logger for discord.
    Creates a new file on midnight UTC time and keeps 7 backups.
    """
    path = r"./logs/tabuu3.log"
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(
        filename=path, when="midnight", backupCount=7, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    logger.addHandler(handler)

    # We also log the really critical stuff to the console, for more visibility.
    console_log = logging.StreamHandler()
    console_log.setLevel(logging.ERROR)
    console_log.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    logger.addHandler(console_log)


def get_logger(name: str) -> logging.Logger:
    """Gets you a descendant of the discord logger.
    That way it's easier when reading the log file to see at a glance where the info came from.
    """
    return logging.getLogger(f"discord.{name}")
