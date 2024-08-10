import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import functools

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

class LoggerClass:
    """
    LoggerClass sets up and manages logging to both file and console with enhanced features.

    Attributes:
        log_level (int): Logging level based on user input.
        silent (bool): Flag to suppress console output.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (logging.Logger): Logger instance for logging messages.
    """

    def __init__(self, log_to_file=True, log_file=None, loglevel='INFO', silent=False, demo=False,
                 max_file_size=0.5 * 1024 * 1024, backup_count=5, log_format=None, log_prefix=f"{os.path.splitext(os.path.basename(__file__))[0]}"):
        """
        Initializes LoggerClass with logging configuration.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
            loglevel (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            silent (bool): Flag to suppress console output.
            demo (bool): Flag to enable demo mode where no actual changes are made.
            max_file_size (int): Maximum size of log file before rotation (default: 10 MB).
            backup_count (int): Number of backup files to keep when rotating.
            log_format (str): Optional custom log format string.
        """
        self.loglevel_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        self.log_to_file = log_to_file
        self.log_file = log_file
        self.log_level = self.loglevel_map.get(loglevel, logging.INFO)
        self.silent = silent
        self.demo = demo
        self.log_prefix = log_prefix

        # Create a logger
        self.logger = logging.getLogger('MyLogger')
        self.logger.setLevel(self.log_level)

        self._setup_handlers(log_to_file, log_file, max_file_size, backup_count, log_format, log_prefix)

    def _setup_handlers(self, log_to_file, log_file, max_file_size, backup_count, log_format, log_prefix):
        """
        Sets up file and console handlers for logging.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
            max_file_size (int): Maximum size of log file before rotation.
            backup_count (int): Number of backup files to keep when rotating.
            log_format (str): Optional custom log format string.
        """
        if not log_format:
            log_format = '%(asctime)s : %(levelname)s -> %(message)s'
        formatter = logging.Formatter(log_format)

        # Set up rotating file handler if needed
        if log_to_file:
            if not log_file:
                log_file = f"{log_prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            self.file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
            self.file_handler.setFormatter(formatter)
            self.logger.addHandler(self.file_handler)

        # Set up console handler if not in silent mode
        if not self.silent:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def set_log_level(self, loglevel):
        """
        Dynamically adjusts the logging level.

        Args:
            loglevel (str): New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        """
        new_level = self.loglevel_map.get(loglevel, logging.INFO)
        self.logger.setLevel(new_level)

    def get_log_files(self):
        # Get the base filename and the list of backup files
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
        # Print the log files before shutting downlog_files = self.get_log_files()
            log_files = self.get_log_files()
            # for i, l in enumerate(log_files):
                # log_files[i] = l.replace(chr(92), '-').replace('-', chr(92))

            self.log_info("*"*80)
            self.log_info(f"*** Log files created: {log_files}")
            self.log_info("*"*80)

        logging.shutdown()


    def __del__(self):
        """
        Shuts down the logger and its handlers gracefully when the object is destroyed.
        """
        self.shutdown()

#    @log_method_call
    def log_message(self, message, level=logging.INFO):
        """
        Logs a message at the specified logging level.

        Args:
            message (str): The message to log.
            level (int): The logging level for the message.
        """
        if self.demo:
            message = f"[DEMO MODE] {message}"
        self.logger.log(level, message)

    # @log_method_call
    # def printlog(self, *args, **kwargs):
    #     """
    #     Logs a message at the default INFO level.

    #     Args:
    #         *x: Variable length argument list for the message.
    #     """
    #     return self.log_message(self, *args, **kwargs)
    
    def log_debug(self, message):
        """Logs a message with DEBUG level."""
        #if self.log_level <= logging.DEBUG:
        self.log_message(message, logging.DEBUG)

    def log_info(self, message):
        """Logs a message with INFO level."""
        #if self.log_level <= logging.INFO:
        self.log_message(message, logging.INFO)

    def log_warning(self, message):
        """Logs a message with ERROR level."""
        #if self.log_level <= logging.WARNING:
        self.log_message(message, logging.WARNING)

    def log_error(self, message):
        """Logs a message with ERROR level."""
        #if self.log_level <= logging.ERROR:
        self.log_message(message, logging.ERROR)

    def log_critical(self, message):
        """Logs a message with CRITICAL level."""
        #if self.log_level <= logging.CRITICAL:
        self.log_message(message, logging.CRITICAL)
