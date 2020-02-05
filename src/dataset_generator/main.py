from argparse import ArgumentParser
from tqdm import tqdm_gui
from src.common import Line, SETTINGS, execute_line_no_loads
from src.common.dialogs import valid_input, valid_choice
from src.common.file_utils import file_dialog
from src.dataset_generator import data
from src.dataset_generator.implementation import add_line, Implementation

generated = []
start_at = 'src\\dataset_generator\\tests'
preview = 100

def main():
    print('Welcome to unofficial dataset generator for key-value 2019 contest.')
    total_lines = valid_input(prompt='Enter dataset size: ', key_formatter=int)
    dataset: data.Dataset = valid_choice(data.datasets, heading='Choose dataset rules')
    data.generate_cmds(dataset)
    data.create_zones(total_lines, dataset)
    progress_bar = tqdm_gui(
        desc='Generating commands',
        total=total_lines,
        position=0,
        leave=False
    )
    order = 1
    for idx, end_of_zone in enumerate(dataset.zones):
        Implementation.cyc_cmd = dataset.cycles_cmds[idx]
        for i in range(order, end_of_zone + 1):
            generated.append(row := add_line())
            execute_line_no_loads(Line(order, row.split(maxsplit=-1 if row[0] == 'H' else 2)))
            progress_bar.update()
            order += 1
    progress_bar.close()
    print(
        f'\n{total_lines} successfully generated.', '\nPreview:\n', 
        *list(generated[:preview]), 
        '...' if total_lines > preview else '', 
        sep='\n'
    )
    file_dialog(generated, prompt='Do you want to save dataset?', start_dir=start_at, ext='txt')
    print('Program will now exit.')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("--base_dir", nargs='?', default=None)
    parser.add_argument("--start_at", nargs='?', default=None)
    args = parser.parse_args()
    if args.debug:
        print('\n\n!!!\nRunning debug configuration.\n!!!\n\n')
    if args.base_dir:
        SETTINGS.BASE_DIR = args.base_dir
    start_at = args.start_at if args.start_at else ''
    main()
