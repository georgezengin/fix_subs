import os
import shutil
import yaml
import json

from misc_utils import _files, _subdirs, _movie_files, _subtitle_files
from movie_class import Movie
from logger_class import LoggerClass  # Import the LoggerClass from its file

class SubtitleManager:
    def __init__(self, logger: LoggerClass, demo: bool):
        """
        Initialize class:
        Args:
            logger (LoggerClass): Logger instance to record the operations.
            demo (bool): Flag to enable demo mode where no actual changes are made. 
        """
        self.logger = logger
        self.demo = demo
        self.sub_ext = '.srt'  # Subtitle file extension

    def find_largest_srt_file(self, folder_path: str, sub_lang: str) -> str:
        """
        Find the largest subtitle file in the specified language.

        Args:
            folder_path (str): Path to the folder containing subtitle files.
            sub_lang (str): Language of the subtitle to look for.

        Returns:
            str: The path of the largest subtitle file found, or None if no files are found.
        """
        # Using the _subtitle_files generator to get subtitle files
        srt_files = [f for f in _subtitle_files(folder_path)] # if sub_lang in f.lower()]
        if not srt_files:
            self.logger.log_debug(f"No subtitle files found in {folder_path}")
            return ''
        self.logger.log_debug(f"{folder_path} Subtitles found: {srt_files}")
        
        largest_file = max(srt_files, key=lambda x: os.path.getsize(os.path.join(folder_path, x)), default='')
        self.logger.log_debug(f"Largest file found: {largest_file}")
        return os.path.join(folder_path, largest_file)

    def manage_subtitles_for_movie(self, movie: Movie) -> bool:
        """
        Manage subtitle files for a given movie.

        Args:
            movie (Movie): The movie object to manage subtitles for.

        Returns:
            bool: True if a subtitle file was successfully found, otherwise False.
        """
        srt_file_path = movie.target_subtitle_path #os.path.join(movie.folder_path, movie.file_name + self.sub_ext)
        if os.path.exists(srt_file_path):
            self.logger.log_debug(f"[{movie.folder_path}]: Subtitle file [{srt_file_path}] already exists.")
            return True

        langs2chk = ['spanish', 'english'] if 'spanish' in movie.file_name.lower() else ['english', 'spanish']

        for sub_lang in langs2chk:
            # check if a subtitle with the same name as the movie already exist, if so, exit and do nothing

            # Check for embedded subtitles first
            if movie.has_embedded_subtitles(sub_lang, self.logger):
                self.logger.log_debug(f"[{movie.folder_path}]: Embedded {sub_lang} subtitles found in [{movie.file_name+movie.file_ext}].")
                return True

            # Look for another subtitle file in the movie's folder and make as target
            largest_file = self.find_largest_srt_file(movie.folder_path, sub_lang)
            if largest_file:
                return movie.set_subtitle_file(largest_file)
            
            # Look for subtitle files in the 'subs' folder
            subs_folder = os.path.join(movie.folder_path, 'subs')
            if os.path.exists(subs_folder):
                largest_file = self.find_largest_srt_file(subs_folder, sub_lang)
                if largest_file:
                    return movie.set_subtitle_file(largest_file)

        self.logger.log_info("="*50)
        self.logger.log_info(f"[{movie.folder_path}]: No suitable subtitle file found for movie [{movie.file_name}].")
        
        return False
