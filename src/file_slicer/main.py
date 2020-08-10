from argparse import ArgumentParser
import sys
from src.common import SETTINGS
from src.common.dialogs import valid_input
from src.common.file_utils import file_dialog

file_path = None
start_at = None

def main():
    total = valid_input(prompt='Enter size of slice: ', key_formatter=int)
    sliced = []
    try:
        with open(file_path) as f:
            for idx, line in enumerate(f):
                if idx == total:
                    break
                sliced.append(line.rstrip('\n'))
    except OSError as e:
        print(repr(e))
        return
    file_dialog(
        sliced, 
        prompt='Do you want to save slice to a file?', 
        start_dir=start_at, 
        ext='txt'
    )

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--base_dir", nargs='?', default=None)
    parser.add_argument("--start_at", nargs='?', default=None)
    parser.add_argument("file_path", nargs='?', default=None)
    args = parser.parse_args()
    if not (file_path := args.file_path):
        print('Bad args: {}'.format(str(argv)))
        sys.exit('__NODATA__')
    if args.base_dir:
        SETTINGS.BASE_DIR = args.base_dir
    start_at = args.start_at if args.start_at else ''
    main()
    print('Program will now exit.')
