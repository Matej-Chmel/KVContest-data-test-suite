"""
Settings for this repository.
"""

import os

class SETTINGS:
    """Settings for this repository.
    """
    BASE_DIR = os.getcwd()
    DECIMAL_PLACES = 2

    @staticmethod
    def setOptions(**kwargs):      
        """Sets settings variables from kwargs dict.
        Keywords:
            BASE_DIR (str): Base directory of file paths.
            DECIMAL_PLACES (int): Number of decimal places to format float numbers.
                Note: this settings is used only in some functions.
        """
        allowed_attrs = SETTINGS.__dict__
        for attr in kwargs:
            if attr in allowed_attrs:
                setattr(SETTINGS, attr, kwargs[attr])
                