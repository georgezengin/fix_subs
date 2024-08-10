import os
import shutil
import json
import yaml

from pymediainfo import MediaInfo
from logger_class import LoggerClass  # Import the LoggerClass from its file

class Movie:
    def __init__(self, movpath: str, demo: bool, logger: LoggerClass):
        self.full_path = movpath
        self.demo = demo
        self.logger = logger

        self.folder_path, self.file_name = os.path.split(movpath)
        self.file_base, self.file_ext = os.path.splitext(self.file_name)
        self.target_subtitle_path = os.path.join(self.folder_path, self.file_base + '.srt')

        #self.logger.log_debug(f"Created Movie object:\n{json.dumps(self.__json__(), indent=4)}")
        # self.logger.log_debug(f"Created Movie object: {yaml.dump(self.__json__())}")

        # self.logger.log_debug(f"Created Movie object: str {self.__str__()}")
        # self.logger.log_debug(f"Created Movie object: yaml {self.__yaml__()}")
        # self.logger.log_debug(f"Created Movie object: repr {self.__repr__()}")
        # self.logger.log_debug(f"Created Movie object: dict {self.__dict__}")
        # self.logger.log_debug(f"Created Movie object: class {self.__class__}")
        # self.logger.log_debug(f"Created Movie object: hash {self.__hash__}")
        # self.logger.log_debug(f"Created Movie object: module {self.__module__}")
        # self.logger.log_debug(f"Created Movie object: doc {self.__doc__}")

    def __str__(self):
        return f"Movie(file_name={self.file_base}, file_ext={self.file_ext}, folder_path={self.folder_path})"
    
    def __json__(self):
        return {
            "full_path": self.full_path,
            "folder_path": self.folder_path,
            "file_name": self.file_name,
            "file_base": self.file_base,
            "file_ext": self.file_ext
        }
    
    def __yaml__(self):
        return yaml.dump(self.__json__())

    def has_embedded_subtitles(self, lang: str, logger: LoggerClass) -> bool:
        """
        Check if the movie has embedded subtitles in the specified language.

        Args:
            lang (str): Language of the subtitle to check for.

        Returns:
            bool: True if embedded subtitles in the specified language are found, otherwise False.
        """
        media_info = MediaInfo.parse(os.path.join(self.folder_path, self.file_name))
        langs = {'english': 'en', 'spanish': 'sp'}

        ret_val = any(track.track_type == 'Text' and 
                      track.language is not None and
                      track.language.lower() == langs[lang]
                        for track in media_info.tracks)
        if len(media_info.tracks) == 0:
            logger.log_debug(f"{self.file_name}: No text tracks found in media file")
        else:
            for track in media_info.tracks:
                if track.track_type == 'Text':
                    logger.log_debug(f"Text Tracks found [{self.file_name}]: Type={track.track_type}, Lang={track.language}, found '{langs[lang]}'?={'Yes' if langs[lang]==track.language else 'Nope'}")
        logger.log_debug(f"{self.file_name}: {'Found' if ret_val else 'Didn\'t find'} embedded subtitles in {lang}: {ret_val}")
        return ret_val

    def set_subtitle_file(self, subtitle_path: str) -> bool:
        """
        Rename or copy the subtitle file to the movie's folder with the name of the target_subtitle path (same as movie with extension .srt).

        Args:
            subtitle_path (str): Path to the subtitle file.

        Returns:
            bool: True if the operation was successful, otherwise False.
        """
        if os.path.exists(self.target_subtitle_path):
            self.logger.log_debug(f"Subtitle already exists at {self.target_subtitle_path}. Skipping.")
            return True

        try:
            if self.demo:
                self.logger.log_debug(f"\tCopying subtitle from [{subtitle_path}] to [{self.target_subtitle_path}]")
            else:
                shutil.copy2(subtitle_path, self.target_subtitle_path)
            self.logger.log_info("="*80)
            self.logger.log_info(f"[{self.folder_path}] Copied subtitle file from [{subtitle_path}] to [{self.target_subtitle_path}]")
        except FileNotFoundError as e:
            self.logger.log_error(f"*** Subtitle file not found: {e} ***")
            return False
        except PermissionError as e:
            self.logger.log_error(f"*** Permission denied: {e} ***")
            return False
        except OSError as e:
            self.logger.log_error(f"*** OS error occurred while copying subtitle file: {e} ***")
            return False
        except Exception as e:
            # Log any other unexpected exceptions
            self.logger.log_error(f"*** Unexpected error occurred: {e} ***")
            return False
        
        return True
