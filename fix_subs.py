import argparse
import os
import sys
from misc_utils import _files, _subdirs, _movie_files, _subtitle_files
from datetime import datetime
from movie_class import Movie
from movie_subtitle_manager import SubtitleManager
from logger_class import LoggerClass


def contains_movie_file(folder_path, logger):
    """
    Checks if the folder contains any movie files based on common movie file extensions.

    Args:
        folder_path (str): The path of the folder to check.

    Returns:
        str: The name of the movie file if found, otherwise None.
    """
    movie_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg'}
    
    for file_name in os.listdir(folder_path):
        movfile = os.path.join(folder_path, file_name)
        if  any(file_name.lower().endswith(ext) for ext in movie_extensions) and \
            os.path.getsize(movfile) > 0 and \
            os.access(movfile, os.R_OK|os.W_OK):
                logger.log_debug(f"Movie file found: [{file_name}]")
                return movfile
    return None

def process_folder(folder_path, recurse, demo, logger):
    """
    Process a folder to find and manage movie files, and their associated subtitles.

    Args:
        folder_path (str): The path of the parent folder.
        recurse (bool): Flag to enable recursive processing of subdirectories.
        demo (bool): Flag to enable demo mode where no actual changes are made.
        logger (LoggerClass): The logger instance for logging messages.
    """

    #folders_to_process = []
    subtitle_manager = SubtitleManager(logger, demo)

    # First pass: run thru dirs and check for movies, if recurse, check subpath if any subdirs with movies
    for folder_name in _subdirs(folder_path):
        if folder_name.lower() == 'subs':
            continue
        subfolder_path = os.path.join(folder_path, folder_name)

        logger.log_debug("\n")
        logger.log_debug("*" * 80)
        logger.log_debug("\n")
        logger.log_debug(f"Folder Path: [{folder_path}] Folder Name: [{folder_name}]")

        movie_file = contains_movie_file(subfolder_path, logger)
        if movie_file:
            #logger.log_debug(f"Folder to process: [{subfolder_path}]")
            #folders_to_process.append(Movie(movie_file, logger))
            subtitle_manager.manage_subtitles_for_movie(Movie(movie_file, demo, logger))

        if recurse:
            # Recursively process subfolders
            process_folder(subfolder_path, recurse, demo, logger)
    
    # Second pass: Process collected directories
    #for movie in folders_to_process:
        

def main(path, log_to_file, logfile, loglevel, silent, demo, recurse):
    """
    Main function to execute the subtitle management process.

    Args:
        path (str): Path to the directory to search for movie files.
        log_to_file (bool): Whether to enable logging to a file.
        logfile (str): Name of the log file, if logging to a file is enabled.
        loglevel (str): Logging level to use (DEBUG, INFO, ERROR).
        silent (bool): Whether to suppress console output.
        demo (bool): Whether to enable demo mode where no actual changes are made.
        recurse (bool): Whether to recursively search subfolders for movie files.
    """
    # Initialize the logger
    logger = LoggerClass(log_to_file=log_to_file, log_file=logfile, loglevel=loglevel, silent=silent, demo=demo, log_prefix=f"{os.path.splitext(os.path.basename(__file__))[0]}")

    logger.log_debug(f"Parameters -> path: {path}")
    logger.log_debug(f"Parameters -> demo: {demo}")
    logger.log_debug(f"Parameters -> log: {log_to_file}")
    logger.log_debug(f"Parameters -> log_file: {logfile}")
    logger.log_debug(f"Parameters -> loglevel: {loglevel}")
    logger.log_debug(f"Parameters -> silent: {silent}" )
    logger.log_debug(f"Parameters -> recurse: {recurse}")
   
    # Validate the path
    #if not path:
    #    folder_path = os.getcwd()

    if not os.path.exists(path):
        logger.log_error(f"Path '{path}' does not exist.")
        sys.exit(1)
    
    path = os.path.abspath(path) # get absolute path

    if not os.path.isdir(path):
        logger.log_error(f"Path '{path}' is not a directory.")
        sys.exit(1)

    logger.log_info(f"folder_path: {path}")
    if logfile:
        logger.log_info(f"Log file: {logfile}")
        if not log_to_file:
            logger.log_info("Log file specified without enabling logging. Enabling logging.")
            log_to_file = True
    if log_to_file:
        logger.log_info(f"Logging enabled, logging level {loglevel}")
    if demo:
        logger.log_info("Demo mode enabled")
    if silent:
        logger.log_info("Silent mode: Console output suppressed")
    logger.log_info(f"{'Recursively s' if recurse else 'S'}earching '{path}' for movie files.")
    logger.log_info("\n")
    
    # Process the directory
    process_folder(path, recurse, demo, logger)
    
def parse_args():
    """
    Parse command line arguments.

    Returns:
        Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Fix subtitles. Run through subfolders and find English srt file in subs if no other subtitle found in folder.")
    
    # Mandatory positional argument
    parser.add_argument('path', type=str, help="Path to the directory to search for movie files.")
    
    # Optional arguments
    parser.add_argument('--log_to_file', '--log', '-L', action='store_true', help="Enable logging to a file.")
    parser.add_argument('--logfile', '-F', type=str, default='', help="Specify log file name.")
    parser.add_argument('--loglevel', '-LL', type=str, choices=['DEBUG', 'INFO', 'ERROR'], default='INFO', help="Set the logging level (DEBUG, INFO, ERROR).")
    parser.add_argument('--silent', '-S', action='store_true', help="Suppress console output.")
    parser.add_argument('--demo', '-D', action='store_true', help="Enable demo mode where no actual changes are made.")
    parser.add_argument('--recurse', '-R', action='store_true', help="Recursively search subfolders for movie files.")
    
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(path=args.path,
         log_to_file=args.log_to_file,
         logfile=args.logfile,
         loglevel=args.loglevel,
         silent=args.silent,
         demo=args.demo,
         recurse=args.recurse)
