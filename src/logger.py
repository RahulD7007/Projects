"""
logger.py
─────────
Centralized logging configuration for the entire project.

Every module obtains its logger via:
    from src.logger import get_logger
    logger = get_logger(__name__)

Log levels
──────────
• DEBUG   – fine-grained pipeline diagnostics
• INFO    – normal operational messages
• WARNING – recoverable anomalies
• ERROR   – failures requiring attention
• CRITICAL– fatal errors

Outputs
───────
• Console  : INFO and above  (coloured StreamHandler)
• File     : DEBUG and above (RotatingFileHandler → logs/pipeline.log)
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
LOGS_DIR: Path = Path(__file__).resolve().parents[1] / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE: Path = LOGS_DIR / "pipeline.log"
FLASK_LOG_FILE: Path = LOGS_DIR / "flask_api.log"

# Max 10 MB per file, keep last 5 rotations
_MAX_BYTES: int = 10 * 1024 * 1024
_BACKUP_COUNT: int = 5

# ─────────────────────────────────────────────────────────────────────────────
# FORMATTERS
# ─────────────────────────────────────────────────────────────────────────────
_DETAILED_FMT = (
    "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
)
_CONSOLE_FMT = "%(asctime)s | %(levelname)-8s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


class _ColourFormatter(logging.Formatter):
    """
    ANSI-coloured console formatter.

    Colours degrade gracefully on terminals that do not support ANSI codes
    (e.g. Windows CMD without ANSI enabled) — formatting falls back to plain
    text automatically.
    """

    _COLOURS: dict[int, str] = {
        logging.DEBUG:    "\033[36m",   # Cyan
        logging.INFO:     "\033[32m",   # Green
        logging.WARNING:  "\033[33m",   # Yellow
        logging.ERROR:    "\033[31m",   # Red
        logging.CRITICAL: "\033[41m",   # Red background
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        colour = self._COLOURS.get(record.levelno, "")
        message = super().format(record)
        # Only apply colour when writing to a real TTY
        if sys.stderr.isatty() if hasattr(sys.stderr, "isatty") else False:
            return f"{colour}{message}{self._RESET}"
        return message


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL SETUP HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _build_logger(
    name: str,
    log_file: Path,
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Create (or retrieve) a named logger with both console and rotating-file
    handlers.  Calling this function multiple times with the same ``name``
    returns the same logger without adding duplicate handlers.

    Parameters
    ----------
    name : str
        Logger name (typically ``__name__`` of the calling module).
    log_file : Path
        Destination path for the rotating log file.
    console_level : int
        Minimum level for console output.
    file_level : int
        Minimum level for file output.

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Guard: do not attach duplicate handlers on re-import
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)   # root level — handlers filter further

    # ── Console handler ───────────────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(
        _ColourFormatter(fmt=_CONSOLE_FMT, datefmt=_DATE_FMT)
    )

    # ── Rotating file handler ─────────────────────────────────────────────────
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(
        logging.Formatter(fmt=_DETAILED_FMT, datefmt=_DATE_FMT)
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False   # prevent double-logging via root logger

    return logger


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def get_logger(name: str) -> logging.Logger:
    """
    Obtain a project-wide logger that writes to ``logs/pipeline.log``.

    Parameters
    ----------
    name : str
        Use ``__name__`` so log records show the originating module.

    Returns
    -------
    logging.Logger

    Examples
    --------
    >>> from src.logger import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("Pipeline started")
    """
    return _build_logger(name, log_file=LOG_FILE)


def get_flask_logger(name: str) -> logging.Logger:
    """
    Obtain a Flask-API-specific logger writing to ``logs/flask_api.log``.

    Parameters
    ----------
    name : str
        Use ``__name__`` of the Flask module.

    Returns
    -------
    logging.Logger
    """
    return _build_logger(name, log_file=FLASK_LOG_FILE)
