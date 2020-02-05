from argparse import ArgumentParser
import os
from sys import argv
import sys
from tqdm import tqdm_gui
from src.common import Line, execute_line_return_result
from src.common.file_utils import file_dialog

dataset_path = None
start_at = None
generated = []
preview = 100

def main():
    try:
        progress_bar = tqdm_gui(
            desc='Solving dataset', 
            total=os.path.getsize(dataset_path),
            position=0,
            leave=False
        )
        with open(dataset_path) as dataset:
            line = None
            for row in dataset:
                line = Line(None, row.rstrip('\n').split(maxsplit=-1 if row[0] == 'H' else 2))
                if(result := execute_line_return_result(line)):
                    generated.append(result)
                progress_bar.update(len(row))
        progress_bar.close()
    except OSError:
        print('Could not open dataset.')
        print(dataset_path)
        progress_bar.close()
        return
    print(
        '\nPreview:\n', 
        *list(generated[:preview]), 
        '...' if len(generated) > preview else '', 
        sep='\n'
    )
    file_dialog(
        generated, 
        prompt='Do you want to save the solution output?', 
        start_dir=start_at, 
        ext='txt'
    )
    print('Program will now exit.')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("--base_dir", nargs='?', default=None)
    parser.add_argument("--start_at", nargs='?', default=None)
    parser.add_argument("dataset_path", nargs='?', default=None)
    args = parser.parse_args()
    if args.dataset_path:
        dataset_path = args.dataset_path
    else:
        print('Only one dataset can be solved at a time.')
        print('Bad args: {}'.format(str(argv)))
        sys.exit('__NODATA__')
    if args.debug:
        print('\n\n!!!\nRunning debug configuration.\n!!!\n\n')
    if args.base_dir:
        SETTINGS.BASE_DIR = args.base_dir
    start_at = args.start_at if args.start_at else ''
    main()
