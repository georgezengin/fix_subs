import os
import re
import argparse
import logging
from datetime import datetime

class LoggerClass:
    """
    LoggerClass sets up and manages logging to both file and console.

    Attributes:
        log_level (int): Logging level based on user input.
        silent (bool): Flag to suppress console output.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (logging.Logger): Logger instance for logging messages.
    """

    def __init__(self, log_to_file, log_file, loglevel, silent, demo):
        """
        Initializes LoggerClass with logging configuration.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
            loglevel (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            silent (bool): Flag to suppress console output.
            demo (bool): Flag to enable demo mode where no actual changes are made.
        """
        loglevel_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        self.log_level = loglevel_map.get(loglevel, logging.INFO)
        self.silent = silent
        self.demo = demo

        # Create a logger
        self.logger = logging.getLogger('MyLogger')
        self.logger.setLevel(self.log_level)

        self._setup_handlers(log_to_file, log_file)

    def _setup_handlers(self, log_to_file, log_file):
        """
        Sets up file and console handlers for logging.

        Args:
            log_to_file (bool): Flag to enable logging to a file.
            log_file (str): The log file name.
        """
        # Create formatters
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Set up file handler if needed
        if log_to_file:
            if not log_file:
                log_file = f"{os.path.splitext(os.path.basename(__file__))[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # Set up console handler if not in silent mode
        if not self.silent:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log_message(self, message, level=logging.INFO):
        """
        Logs a message at the specified logging level.

        Args:
            message (str): The message to log.
            level (int): The logging level for the message.
        """
        self.logger.log(level, message)

def validate_folder_path(folder_path, logger):
    """
    Validates the given folder path.

    Args:
        folder_path (str): The folder path to validate.
        logger (LoggerClass): The logger instance for logging messages.

    Returns:
        bool: True if the folder path is valid, False otherwise.
    """
    if not os.path.exists(folder_path):
        logger.log_message(f"The folder path [{folder_path}] does not exist.", logging.ERROR)
        return False
    
    if not os.path.isdir(folder_path):
        logger.log_message(f"The path [{folder_path}] is not a directory.", logging.ERROR)
        return False
    
    return True

def analyze_folder_name(folder_name, use_rest_of_name, logger):
    """
    Analyzes and formats the folder name based on year patterns.

    Args:
        folder_name (str): The folder name to analyze.
        use_rest_of_name (bool): Flag to use the rest of the name after the year.
        logger (LoggerClass): The logger instance for logging messages.

    Returns:
        str: The new folder name if a year pattern is found, None otherwise.
    """
    logger.log_message(f"Analyzing folder name: [{folder_name}]", logging.DEBUG)

    # Regular expression pattern to match year
    year_pattern = re.compile(r"(?<=\.)((19|20)\d{2})(?=\.)|(?<=\()((19|20)\d{2})(?=\))")
    
    matches = list(year_pattern.finditer(folder_name))
    
    if matches:
        # Get the last match object
        last_match = matches[-1]
        year_match = last_match.group(0)
        year_start = last_match.start()
        year_end = last_match.end()
        logger.log_message(f"Match found: year_match={year_match} in '{folder_name}'", logging.DEBUG)
    else:
        logger.log_message(f"No year pattern found in '{folder_name}'.", logging.DEBUG)
        return None

    # Extract and keep the original 'before_year' and 'after_year' logic
    before_year = (folder_name[:year_start-2].replace('.', ' ') +  
                   folder_name[year_start-2:year_start].replace(' (','')).strip()
    before_year = before_year.replace('.',' ').replace('  ',' ').strip() 
    logger.log_message(f"-- Before_year=[{before_year}].", logging.DEBUG)

    new_folder_name = f"{before_year} ({year_match})"
    logger.log_message(f"-- new_folder_name=[{new_folder_name}].", logging.DEBUG)

    if use_rest_of_name:
        after_year = folder_name[year_end+1:].strip().replace("[", "").replace("]", "").replace(". ", ".").replace(" ", ".")
        logger.log_message(f"-- after_year=[{after_year}].", logging.DEBUG)
        if after_year:
            new_folder_name += f" [{after_year}]"

    logger.log_message(f"New folder name: [{new_folder_name}]" if new_folder_name != folder_name else "--->>> Folder not changed <<<---", logging.DEBUG)
    return new_folder_name if new_folder_name != folder_name else None

def rename_folder(folder_path, old_name, new_name, demo, logger):
    """
    Renames a folder from old_name to new_name.

    Args:
        folder_path (str): The path of the parent folder.
        old_name (str): The current folder name.
        new_name (str): The new folder name.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (LoggerClass): The logger instance for logging messages.
    """
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)
    counter = 1

    logger.log_message(f'Renaming "{old_name}" to "{new_name}" in [{folder_path}]', logging.INFO)

    while os.path.exists(new_path):
        new_path = os.path.join(folder_path, f"{new_name} ({counter})")
        counter += 1

    if not demo:
        try:
            os.rename(old_path, new_path)
            logger.log_message(f"Renamed [{os.path.basename(new_path)}]", logging.INFO)
        except PermissionError:
            logger.log_message(f"Permission denied when renaming [{old_name}] to [{new_name}].", logging.ERROR)
        except OSError as e:
            logger.log_message(f"An OS error occurred while renaming [{old_name}] to [{new_name}]: {e}", logging.ERROR)
        except Exception as e:
            logger.log_message(f"An unexpected error occurred: {e}", logging.ERROR)
    else:
        logger.log_message(f"Debug mode: Rename [{old_name}] => [{new_name}]", logging.DEBUG)

def contains_movie_file(folder_path):
    """
    Checks if the folder contains any movie files based on common movie file extensions.

    Args:
        folder_path (str): The path of the folder to check.

    Returns:
        bool: True if the folder contains movie files, False otherwise.
    """
    # Define movie file extensions
    movie_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg'}
    
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            if any(file_name.lower().endswith(ext) for ext in movie_extensions):
                return True
    return False

def process_folder(folder_path, use_rest_of_name, demo, logger, recurse):
    """
    Processes the folder to rename subdirectories containing movie files.

    Args:
        folder_path (str): The path of the parent folder.
        use_rest_of_name (bool): Flag to use the rest of the name after the year.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (LoggerClass): The logger instance for logging messages.
        recurse (bool): Flag to enable recursive processing of subdirectories.
    """
    # Collect directories to process in a list
    directories_to_process = []

    # First pass: Collect all directories and check if they contain movie files
    for folder_name in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, folder_name)

        if os.path.isdir(subfolder_path):
            if contains_movie_file(subfolder_path):
                logger.log_message(f"Folder to process: [{folder_name}]", logging.DEBUG)
                directories_to_process.append((folder_path, folder_name))

            if recurse:
                # Recursively process subfolders
                process_folder(subfolder_path, use_rest_of_name, demo, logger, recurse)
    
    # Second pass: Process collected directories
    for parent_folder, folder_name in directories_to_process:
        new_folder_name = analyze_folder_name(folder_name, use_rest_of_name, logger)
        if new_folder_name:
            rename_folder(parent_folder, folder_name, new_folder_name, demo, logger)

def main(folder_path, use_rest_of_name, demo, log, log_file, loglevel, silent, recurse):
    """
    Main function to initiate the renaming process based on user inputs.

    Args:
        folder_path (str): The path of the folder containing the directories to rename.
        use_rest_of_name (bool): Flag to use the rest of the name after the year.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        log (bool): Flag to enable logging.
        log_file (str): The log file name.
        loglevel (str): Logging level (DEBUG, INFO, ERROR).
        silent (bool): Flag to suppress console output.
        recurse (bool): Flag to enable recursive processing of subdirectories.
    """
    logger = LoggerClass(log, log_file, loglevel, silent, demo)

    logger.log_message("\n", logging.INFO)
    logger.log_message("*" * 80, logging.INFO)
    logger.log_message("\n", logging.INFO)

    logger.log_message(f"Parameters -> folder_path: {folder_path}", logging.DEBUG)
    logger.log_message(f"Parameters -> use_rest_of_name: {use_rest_of_name}", logging.DEBUG)
    logger.log_message(f"Parameters -> demo: {demo}", logging.DEBUG)
    logger.log_message(f"Parameters -> log: {log}", logging.DEBUG)
    logger.log_message(f"Parameters -> log_file: {log_file}", logging.DEBUG)
    logger.log_message(f"Parameters -> loglevel: {loglevel}", logging.DEBUG)
    logger.log_message(f"Parameters -> silent: {silent}", logging.DEBUG )
    logger.log_message(f"Parameters -> recurse: {recurse}", logging.DEBUG)
   
    if not folder_path:
        folder_path = os.getcwd()

    if not validate_folder_path(folder_path, logger):
        return
    logger.log_message(f"folder_path: {folder_path}", logging.INFO)

    if log_file:
        logger.log_message(f"Log file: {log_file}", logging.INFO)
        if not log:
            logger.log_message("Log file specified without enabling logging. Enabling logging.", logging.INFO)
            log = True
    if log:
        logger.log_message(f"Logging enabled, logging level {loglevel}", logging.INFO)
    if demo:
        logger.log_message("Demo mode enabled", logging.INFO)
    if not use_rest_of_name:
        logger.log_message("Remove release description when found (resolution, release group, language, etc)", logging.INFO)
    if silent:
        logger.log_message("Silent mode: Console output suppressed", logging.INFO)
    if recurse:
        logger.log_message("Traverse mode: Traverse through subfolders", logging.INFO)

    process_folder(folder_path, use_rest_of_name, demo, logger, recurse)

    logger.log_message("\n", logging.INFO)
    logger.log_message("*" * 80, logging.INFO)
    logger.log_message("\n", logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename movie folders by extracting and formatting name, years and release description as <name> (year) [release_description].")
    parser.add_argument('folder_path', type=str, nargs='?', default=os.getcwd(), help="Path to the folder containing the directories to rename")
    parser.add_argument('--nodesc', '-S', action='store_true', help="Short name. Do not append movie release description after the year")
    parser.add_argument('--demo', '-D', action='store_true', help="Demo mode. Show actions without performing them")
    parser.add_argument('--log', '-L', action='store_true', help="Enable logging")
    parser.add_argument('--logfile', '-F', type=str, help="Log file name (self generated if not specified)")
    parser.add_argument('--loglevel', '-LL', choices=['DEBUG', 'INFO', 'ERROR'], default='INFO', help="Set logging level")
    parser.add_argument('--silent', '-H', action='store_true', help="Silent/hush mode: suppress console output of log information")
    parser.add_argument('--recurse', '-R', action='store_true', help="Recursive mode: traverses through subfolders")

    args = parser.parse_args()
    main(args.folder_path, not args.nodesc, args.demo, args.log, args.logfile, args.loglevel, args.silent, args.recurse)
