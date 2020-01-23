"""
Settings for this repository.
Calling setOptions() before using any of the common modules is recommended.
"""

class SETTINGS:
    """Settings for this repository.
    Calling setOptions() before using any of the common modules is recommended.
    """
    BASE_DIR = '__DIRECTORY_NOT_SET__'

    @staticmethod
    def setOptions(**kwargs):      
        """Sets global variables from attribute dict.

        Args:
            BASE_DIR (str): Base directory of file paths.
        """        
        allowed_attrs = SETTINGS.__dict__
        for attr in kwargs:
            if attr in allowed_attrs:
                setattr(SETTINGS, attr, kwargs[attr])
                