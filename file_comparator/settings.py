'''
Global settings for chm__ module.
Calling setOptions before using chm__ is recommended.
'''

class MCHM_SETTINGS:
    """Global settings for chm__ module.
    Calling setOptions before using chm__ is recommended.
    """
    BASE_DIR = '___DIRECTORY_NOT_SET___'

    @staticmethod
    def setOptions(**kwargs):      
        """Sets global variables from attribute dict.

        Args:
            BASE_DIR (str): Base directory of caller.
                from os.path import dirname, realpath
                dirname(realpath(__file__))
        """        
        allowed_attrs = MCHM_SETTINGS.__dict__
        for attr in kwargs:
            if attr in allowed_attrs:
                setattr(MCHM_SETTINGS, attr, kwargs[attr])
                