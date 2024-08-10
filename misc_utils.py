import os
from collections.abc import Generator

def _subdirs(root: str) -> Generator[str, None, None]:
    """
    Yield the names of subdirectories within the specified root directory.

    Args:
        root (str): The path of the root directory to search.

    Yields:
        str: Name of each subdirectory within the root directory.
    """
    for file in os.listdir(root):
        if os.path.isdir(os.path.join(root, file)):
            yield file

def _files(root: str) -> Generator[str, None, None]:
    """
    Yield the names of files within the specified root directory.

    Args:
        root (str): The path of the root directory to search.

    Yields:
        str: Name of each file within the root directory.
    """
    for file in os.listdir(root):
        if os.path.isfile(os.path.join(root, file)):
            yield file

def _movie_files(root: str) -> Generator[str, None, None]:
    """
    Yield the names of movie files within the specified root directory, 
    filtered by common movie file extensions.

    Args:
        root (str): The path of the root directory to search.

    Yields:
        str: Name of each movie file within the root directory, with extensions 
             like .mp4, .mkv, .avi, .mov, .wmv, .flv, .mpeg, .mpg.
    """
    movie_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.mpeg', '.mpg'}
    for file in _files(root):
        if any(file.lower().endswith(ext) for ext in movie_extensions):
            yield file

def _subtitle_files(root: str) -> Generator[str, None, None]:
    """
    Yield the names of subtitle files within the specified root directory, 
    filtered by common subtitle file extensions.

    Args:
        root (str): The path of the root directory to search.

    Yields:
        str: Name of each subtitle file within the root directory, with extensions 
             like .srt, .sub, .vtt.
    """
    sub_extensions = {'.srt', '.sub', '.vtt'}
    for file in _files(root):
        if any(file.lower().endswith(ext) for ext in sub_extensions):
            yield file
