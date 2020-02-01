from argparse import ArgumentParser
import os
from sys import argv
import sys
from tqdm import tqdm_gui
from src.common import Line, execute_line_no_loads
import src.dataset_analyzer.stats as stats

desired_stats = [
    #stats.CommandPercentage(),
    #stats.CommandTimeline(1),
    #stats.HashloadInfo(),
    #stats.CommandChain(),
    #stats.KeyLengths(),
    stats.KeyDistances(),
]
dataset_path = None

#TODO: get BASE_DIR of shortcut (caller of run.bat)
def main():
    activator = stats.Activator(desired_stats)
    try:
        progress_bar = tqdm_gui(
            desc='Computing statistics', 
            total=os.path.getsize(dataset_path),
            position=0,
            leave=False
        )
        with open(dataset_path) as dataset:
            order = 1
            line = None
            for row in dataset:
                line = Line(order, row.rstrip('\n').split(maxsplit=-1 if row[0] == 'H' else 2))
                for stat in activator.active_stats[line.cmd]:
                    stat(line)
                execute_line_no_loads(line)
                order += 1
                progress_bar.update(len(row))
            for end_func in activator.end_dataset:
                end_func(line)
        progress_bar.close()
    except OSError:
        print('Could not open dataset.')
        print(dataset_path)
        return
    for writer in activator.console_output:
        print(writer())
    for graph in activator.graph_output:
        graph()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--debug", action='store_true', default=False)
    parser.add_argument("dataset_path", nargs='?', default=None)
    args = parser.parse_args()
    if args.debug:
        print('\n\n!!!\nRunning debug configuration.\n!!!\n\n')
    if args.dataset_path:
        dataset_path = args.dataset_path
    else:
        print('Only one dataset can be analyzed at a time.')
        print('Bad args: {}'.format(str(argv)))
        sys.exit('__NODATA__')
    main()
