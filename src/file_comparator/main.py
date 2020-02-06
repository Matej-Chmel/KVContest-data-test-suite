from argparse import ArgumentParser
from itertools import zip_longest
import os
from sys import argv
import sys
from tqdm import tqdm_gui
from src.common import SETTINGS, PREVIEW
from src.common.file_utils import file_dialog

sources: list = None
start_at: str = None
diff = []

def main():
    file_info = [f'{idx + 1}: {item}' for idx, item in enumerate(sources)]
    print(*file_info, sep='\n', end='\n\n')
    progress_bar = None
    try:
        max_size = max(map(os.path.getsize, sources))
        progress_bar = tqdm_gui(
            desc='Finding differences in files', 
            total=max_size,
            position=0,
            leave=False
        )
        print(end=(newline := '\n'))
        with open(sources[0]) as file0:
            with open(sources[1]) as file1:
                for idx, (line0, line1) in enumerate(zip_longest(file0, file1, fillvalue='')):
                    order = idx + 1
                    if line0 != line1:
                        msg = [' -> OK', ' -> OK']
                        for num, line in enumerate([line0, line1]):
                            if not line:
                                msg[num] = ' -> Line is missing.'
                                break
                            if line[-1] != '\n':
                                msg[num] = ' -> Final newline is missing.'
                                break
                        else:
                            msg[0], msg[1] = ': ' + line0.rstrip('\n'), ': ' + line1.rstrip('\n')
                        diff.extend([
                            f'{order}{msg[0]}',
                            f'{order}{msg[1]}{newline}'
                        ])
        progress_bar.close()
    except OSError as e:
        print(f'System encountered an error while opening files.\n{repr(e)}')
        if progress_bar:
            progress_bar.close()
        return
    if not diff:
        print('No differences were found.')
        return
    print('Preview of found differences:\n', *list(diff[:PREVIEW]), sep='\n')
    if len(diff) > PREVIEW:
        print('...\n')
    diff.insert(0, file_info[1] + '\n')
    diff.insert(0, file_info[0])
    diff[-1] = diff[-1].rstrip('\n')
    file_dialog(
        diff, 
        prompt='Do you want to save the differences to a file?', 
        start_dir=start_at, 
        ext='txt'
    )

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("--base_dir", nargs='?', default=None)
    parser.add_argument("--start_at", nargs='?', default=None)
    parser.add_argument("files", nargs='*', default=None)
    args = parser.parse_args()
    if not args.files or len(args.files) != 2:
        print('Exactly two files can be compared at a time.')
        print('Bad args: {}'.format(str(argv)))
        sys.exit('__NODATA__')
    sources = args.files
    if args.debug:
        print('\n\n!!!\nRunning debug configuration.\n!!!\n\n')
    if args.base_dir:
        SETTINGS.BASE_DIR = args.base_dir
    start_at = args.start_at if args.start_at else ''
    main()
    print('Program will now exit.')
