#import logging
import os
import sys
import logging
import functools
from datetime import datetime

from pathlib import Path

from logging.handlers import RotatingFileHandler

class LoggerClass:
    """
    LoggerClass sets up and manages logging to both file and console with enhanced features.

    Attributes:
        log_level (int): Logging level based on user input.
        silent (bool): Flag to suppress console output.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (logging.Logger): Logger instance for logging messages.
    """

    def __init__(self, log_to_file: bool = True, log_file: str = None, loglevel: str = 'INFO', silent: bool = False, demo: bool = False,
                 max_file_size: int = 0.5 * 1024 * 1024, backup_count: int = 5, file_log_format: str = None, console_log_format: str = None, log_prefix: str = f"{os.path.splitext(os.path.basename(__file__))[0]}"):
        """
        Initializes LoggerClass with logging configuration.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
            loglevel (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            silent (bool): Flag to suppress console output.
            demo (bool): Flag to enable demo mode where no actual changes are made.
            max_file_size (int): Maximum size of log file before rotation (default: 0.5 MB).
            backup_count (int): Number of backup files to keep when rotating.
            file_log_format (str): Optional custom log format string for file.
            console_log_format (str): Optional custom log format string for console.
            log_prefix (str): Prefix to use for auto-generated log names (default: the main calling file name).
        """
        self.loglevel_map = logging.getLevelNamesMapping()

        self.log_to_file = log_to_file
        self.log_file = log_file

        self.loglevel = loglevel.upper()
        self.log_level = self.loglevel_map.get(loglevel, logging.INFO)
        # silent = if True, will suppress printing log to console
        self.silent = silent
        # demo - if demo mode, prefix every entry with contents of demo_prefix [DEMO]
        self.demo = demo
        self.demo_prefix = '[DEMO MODE] ' if demo else ''
        # prefix to use for auto-generated log names (by default - the main calling file name)
        self.log_prefix = log_prefix

        # Create a logger
        self.logger = logging.getLogger('MyLogger')
        self.logger.setLevel(self.log_level)

        self._setup_handlers(log_to_file, log_file, max_file_size, backup_count, file_log_format, console_log_format, log_prefix)

    def __del__(self):
        """
        Shuts down the logger and its handlers gracefully when the object is destroyed.
        """
        self.shutdown()

    def _setup_handlers(self, log_to_file: bool, log_file: str, max_file_size: int, backup_count: int, file_log_format: str, console_log_format: str, log_prefix: str):
        """
        Sets up file and console handlers for logging.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
            max_file_size (int): Maximum size of log file before rotation.
            backup_count (int): Number of backup files to keep when rotating.
            file_log_format (str): Optional custom log format string for file.
            console_log_format (str): Optional custom log format string for console.
            log_prefix (str): Prefix for auto-generated logs, a timestamp is appended to this prefix.
        """
        # Set up rotating file handler if needed
        if log_to_file:
            if not file_log_format:
                file_log_format = "{asctime} [{levelname:^5}] -> {message}"
            file_formatter = logging.Formatter(fmt=file_log_format, datefmt="%Y-%m-%d %H:%M:%S", style="{")

            if not log_file:
                log_file = f"{log_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

            self.file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
            self.file_handler.setFormatter(file_formatter)
            self.logger.addHandler(self.file_handler)

        # Set up console handler if not in silent mode
        if not self.silent:
            if not console_log_format:
                #console_log_format = "%(asctime)s %(levelname)s -> %(message)s"
                console_log_format = "{asctime} {levelname:^5} {message}"
                #log_format = "%(asctime)s :: %(levelname)s :: %(name)s :: %(filename)s :: %(lineno)d :: %(message)s"

            self.console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = ColoredFormatter(fmt=console_log_format, datefmt="%Y-%m-%d %H:%M:%S", style="{", demo=self.demo)
            # #console_formatter = logging.Formatter(fmt=console_log_format, datefmt="%Y-%m-%d %H:%M:%S", style="{")
            # console_formatter = DebugFormatter(fmt=console_log_format, datefmt="%Y-%m-%d %H:%M:%S", style="%")
            self.console_handler.setFormatter(console_formatter)
            self.logger.addHandler(self.console_handler)

    def set_log_level(self, loglevel: str):
        """
        Dynamically adjusts the logging level.

        Args:
            loglevel (str): New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        new_level = self.loglevel_map.get(loglevel, logging.INFO)
        self.logger.setLevel(new_level)

    def get_log_files(self) -> list[str]:
        """
        Retrieves the list of log files including backups.

        Returns:
            list[str]: List of log file paths.
        """
        log_files = [self.file_handler.baseFilename]

        # Add rotated log files based on backup count
        for i in range(1, self.file_handler.backupCount + 1):
            rotated_log_file = f"{self.file_handler.baseFilename}.{i}"
            if os.path.exists(rotated_log_file):
                log_files.append(rotated_log_file)

        return log_files

    def shutdown(self):
        """
        Shuts down the logger and its handlers gracefully.
        """
        for handler in self.logger.handlers:
            handler.flush()

        if self.log_to_file:
            # Print the log files before shutting down
            log_files = self.get_log_files()
            # for i, l in enumerate(log_files):
                # log_files[i] = l.replace(chr(92), '-').replace('-', chr(92))

            self.log_info('')
            self.log_info(f"*** Log file{'s' if len(log_files) != 1 else ''} created: {log_files}")
            self.log_info('')

        logging.shutdown()

    # def log_method_call(method):
    #     @functools.wraps(method)
    #     def wrapper(self, *args, **kwargs):
    #         func_name = method.__name__
    #         expected_args = method.__code__.co_argcount
    #         actual_args = len(args)
    #         if actual_args != expected_args:
    #             raise TypeError(
    #                 f"Class:'{self.__class__.__name__}' method:'{func_name}'  "
    #                 f"expected {method.__code__.co_argcount} arguments, got {len(args)}"
    #             )
    #         return method(self, *args, **kwargs)
    #     return wrapper

    # @log_method_call
    def log_message(self, message: str, level: int = logging.INFO):
        """
        Logs a message at the specified logging level.

        Args:
            message (str): The message to log.
            level (int): The logging level for the message.
        """
        import textwrap
        import shutil
        
#        if self.demo:
#            message = f"{self.demo_prefix}{message}"
        # Get console width and subtract 20 for chunking
        console_width = shutil.get_terminal_size((132, 24)).columns
        #console_height = shutil.get_terminal_size((132, 24)).lines
        #print(f"{console_width=} {console_height=}")
        padding_width = console_width - 35  # The desired width for centering
        padding_char = ' '  # The character to use for padding
        # Split the message into chunks
        message_chunks = textwrap.wrap(message, width=padding_width)

        # Log each chunk separately
        for i, chunk in enumerate(message_chunks):
            #if self.demo: # and self.log_level < logging.INFO:
            # Add padding and center the chunk
            #print('123456789+'*(console_width//10))
            chunk = f"{self.demo_prefix}{chunk.ljust(padding_width - len(self.demo_prefix), padding_char)}"
            self.logger.log(level, chunk)

    def get_demo_prefix(self) -> str:
        return self.demo_prefix
    
    def set_demo_prefix(self, prefix: str):
        self.demo_prefix = prefix

    def get_log_level(self) -> int:
        return self.log_level

    def get_loglevel(self) -> str:
        return self.loglevel

    def get_demo(self) -> bool:
        return self.demo

    # @log_method_call
    # def printlog(self, *args, **kwargs):
    #     """
    #     Logs a message at the default INFO level.

    #     Args:
    #         *x: Variable length argument list for the message.
    #     """
    #     return self.log_message(self, *args, **kwargs)

    def log_debug(self, message: str):
        """Logs a message with DEBUG level."""
        #if self.log_level <= logging.DEBUG:
        self.log_message(message, logging.DEBUG)

    def log_info(self, message: str):
        """Logs a message with INFO level."""
        #if self.log_level <= logging.INFO:
        self.log_message(message, logging.INFO)

    def log_warning(self, message: str):
        """Logs a message with ERROR level."""
        #if self.log_level <= logging.WARNING:
        self.log_message(message, logging.WARNING)

    def log_error(self, message: str):
        """Logs a message with ERROR level."""
        #if self.log_level <= logging.ERROR:
        self.log_message(message, logging.ERROR)

    def log_critical(self, message: str):
        """Logs a message with CRITICAL level."""
        #if self.log_level <= logging.CRITICAL:
        self.log_message(message, logging.CRITICAL)

from termcolor import colored
from colorama import init as clr_init

# Initialize colorama to support ANSI codes on Windows
clr_init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter to add color to log messages based on log level."""
    
    # Define a dictionary mapping log levels to color settings (asctime, level, message) to use with colored instruction from termcolor library
    LOG_COLORS = {
            logging.DEBUG:   ( ('light_yellow', None, []),    ('light_green', None, []),     ('light_yellow', None, []) ),
            logging.INFO:    ( ("light_yellow", None, []),    ('white', None, []),           ('white', None, []) ),
            logging.WARNING: ( ('yellow', None, []),          ('yellow', None, []),          ('light_yellow', None, []) ),
            logging.ERROR:   ( ('light_red', None, ['bold']), ('light_red', None, ['bold']), ('light_red', None, ['bold']) ),
            logging.CRITICAL:( ('white', 'on_red', ['bold']), ('white', 'on_red', ['bold']), ('white', 'on_red', ['bold']) ),
            logging.FATAL:   ( ('white', 'on_red', ['bold']), ('white', 'on_red', ['bold']), ('white', 'on_red', ['bold']) )
        }

    def __init__(self, fmt: str = "%(asctime)s %(levelname)s -> %(message)s", datefmt: str = "%Y-%m-%d %H:%M:%S",
                 style: str = "%", demo: bool = False):
        """
        Initialize the formatter with optional formatting strings and demo mode.
        
        :param fmt: Format string for the log message.
        :param datefmt: Format string for the date in log messages.
        :param style: Style of the format string.
        :param demo: If True, applies color to the log message content (message) for demonstration purposes.
        """
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.demo = demo

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        """
        Override formatTime to include milliseconds.
        
        :param record: The log record to format.
        :param datefmt: Optional date format string.
        :return: The formatted time string with milliseconds.
        """
        dt = datetime.fromtimestamp(record.created)
        # Format time with milliseconds (fractional seconds)
        return dt.strftime(datefmt) + f".{int(dt.microsecond / 10000):02d}"
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with color coding based on log level.
        
        :param record: The log record to format.
        :return: The formatted log record string.
        """
        # seems to be a bug in the logging library, the attribute <asctime> is not part of the record, so we add it if its not there
        if not hasattr(record, 'asctime'):
            record.asctime = self.formatTime(record, self.datefmt)

        # Apply color settings based on log level
        levelno = record.levelno
        colors = self.LOG_COLORS.get(levelno, (None, None, []))  # Retrieve the tuple for the given log level

            # Retrieve color settings based on the log level for each part of the log record
        color, on_color, attrs = colors[0]
        if color or on_color or attrs:
            # Debug: Print what color settings are being applied
            # print(f"Debug: asctime={record.asctime}, color={asctime_color}, on_color={asctime_on_color}, attrs={asctime_attrs} {colored(record.asctime, asctime_color)=}")
            record.asctime = colored(record.asctime, color, on_color, attrs)
        
        color, on_color, attrs = colors[1]
        if color or on_color or attrs:
            if self.demo:
                if 'reverse' not in attrs:
                    attrs.append('reverse')
                if levelno == logging.DEMO:
                    record.levelname = colored(f"{f"{record.levelname} ({record.levelno})":^10}", color, on_color, attrs)
            else:
                record.levelname = colored(f"{f"{record.levelname}":^7}", color, on_color, attrs)

        color, on_color, attrs = colors[2]
        if color or on_color or attrs:
            #print(f"Debug: {record.msg=}, {color=}, {on_color=}, {attrs=} {colored(record.msg, color, on_color, attrs)=}")
            record.msg = colored(record.msg, color, on_color, attrs) #if record.levelno < logging.INFO else record.msg
        
        return super().format(record)

# class DebugFormatter(logging.Formatter):

#     def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
#         """
#         Override formatTime to include milliseconds.
        
#         :param record: The log record to format.
#         :param datefmt: Optional date format string.
#         :return: The formatted time string with milliseconds.
#         """
#         dt = datetime.fromtimestamp(record.created)
#         # Format time with milliseconds (fractional seconds)
#         return dt.strftime(datefmt) + f".{int(dt.microsecond / 10000):02d}"

#     def format(self, record: logging.LogRecord) -> str:
#         # Print all available attributes
#         import json
#         print(f"Debug: record attributes: {json.dumps(vars(record))}")
#         if not hasattr(record, 'asctime'):
#             print('No ASCTIME')
#             record.asctime = self.formatTime(record, self.datefmt)
#         print(f"Debug: asctime={record.asctime}, {json.dumps(vars(record))}")

#         return super().format(record)
