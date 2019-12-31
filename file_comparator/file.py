'''
File utility.
'''
from os.path import isfile
from settings import MCHM_SETTINGS as g

def create_file_from_lines(lines, filename, ext=''):
    """Creates new file from text lines. If file already exists, nothing happens.
    
    Args:
        lines (iterable): Text data.
        filename (str): Filename without extension.
        ext (str, optional): File extension. Defaults to ''.
    
    Returns:
        bool: Returns true if new file was created. False if such file already existed.
    """    
    filename += '.{}'.format(ext)
    fullname = '{0}/{1}'.format(g.BASE_DIR, filename)
    # file already exists
    if isfile(fullname):
        print('File {} already exists.'.format(fullname))
        return False
    try:
        with open(filename, "w+") as datafile:
            datafile.write('\n'.join(lines) + '\n')
    except EnvironmentError:
        print('Could not open file {}'.format(fullname))
        return False
    # file written
    return True
