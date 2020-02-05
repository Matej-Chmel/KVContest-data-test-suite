from os.path import isfile
from pathlib import Path
from src.common import SETTINGS
from src.common.dialogs import yes_no

def get_file_path(filename, ext='', start_dir='') -> str:
    """
    Args:
        filename (str): File name without extension.
        ext (str) opt: File extension.
        start_dir (str) opt: Path to start directory from SETTINGS.BASE_DIR.
    Returns:
        str: Prepends SETTINGS.BASE_DIR to full file name.
    """
    return '{}\\{}{}{}'.format(
        SETTINGS.BASE_DIR,
        start_dir + '\\' if start_dir else '',
        filename,
        '.' + ext if ext else ''
    )

def file_exists(path) -> bool:
    """Returns whether there is file on path.
    Args:
        path (str): Full path.
    Returns:
        bool: Whether file exists.
    """    
    return isfile(path)

def ensure_folder(path):
    """Makes sure folder exists.
    Args:
        path (str): Full path.
    """    
    Path(path).mkdir(parents=True, exist_ok=True)

def write_file_from_lines(lines, path) -> bool:
    """Write to file with creation permissions.
    Args:
        lines (list): List of lines.
        path (str | bytes | int): Full path to be passed to open() function.
    Returns:
        bool: Whether writing was a success.
    """
    try:
        with open(path, "w+") as f:
            f.write('\n'.join(lines) + '\n')
    except EnvironmentError as e:
        print(f'Could not write to file {path}\n{repr(e)}')
        return False
    print(f'File was successfully written. Path:\n{path}')
    return True

def file_dialog(lines, prompt='', start_dir='', ext=''):
    """Ensures existence of start_dir and prompts user for file name.
    Then attempts to write lines into that file.
    Args:
        lines (list): List of lines.
        prompt (str) opt: Prompt for user.
        start_dir (str) opt: Path to start directory from SETTINGS.BASE_DIR.
        ext (str) opt: File extension.
    """
    ensure_folder(get_file_path('', start_dir=start_dir))
    while True:
        if yes_no(prompt):
            filename = input('Enter filename without extension: ')
            path = get_file_path(filename, ext=ext, start_dir=start_dir)
            if file_exists(path):
                print('Such file already exists.')
                if yes_no('Do you want to overwrite this file?'):
                    if write_file_from_lines(lines, path):
                        break
            elif write_file_from_lines(lines, path):
                break
        else:
            break

if __name__ == "__main__":
    lines = [
        'aaaaaaaa',
        'bbbbbbbb',
        'ccc',
        'ddd\nddd'
    ]
    print(get_file_path('abc', 'txt', ''))
    file_dialog(lines, prompt='Save test file?', ext='txt', start_dir='src\\common\\test')
    