'''
Test script.
'''

from os.path import dirname, realpath
from settings import MCHM_SETTINGS as g
from prompt import create_file_prompt

def main():
    g.setOptions(BASE_DIR=dirname(realpath(__file__)))
    data = [
        'line 1',
        'line 2',
        'line 3',
        'line 4',
        'line 5',
    ]
    print(create_file_prompt('Do you want to save a file?', data, ext='txt'))

if __name__ == "__main__":
    main()