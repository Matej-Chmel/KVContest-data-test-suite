from sys import argv
from stats import Line
import stats
#from ..common.settings import SETTINGS

active = [
    stats.CommandPercentage
]

alrs = []
h = []

#TODO: get BASE_DIR of shortcut (caller of run.bat)
def main():
    if len(argv) != 2:
        print('Only one dataset can be analyzed at a time.')
        print('Bad args: {}'.format(str(argv)))
        return
    for comp in active:
        if issubclass(comp, stats.ALRS):
            alrs.append(comp)
        if issubclass(comp, stats.H):
            h.append(comp)
    try:
        with open(argv[1]) as dataset:
            i = 1
            for line_str in dataset:
                if line_str[0] == 'H':
                    line_obj = Line(i, line_str.split())
                    for comp in h:
                        comp.compute_h(line_obj)
                else:
                    line_obj = Line(i, line_str.split(maxsplit=2))
                    for comp in alrs:
                        comp.compute_alsr(line_obj)
                stats.execute_line(line_obj)
                i += 1
    except OSError:
        print('Could not open dataset.')
        print(argv[1])
        return
    for item in active:
        print(item.get_output())

if __name__ == "__main__":
    #debug
    #argv.append('D:\\MATEJ\\DEV\\Python\\School\\KVContest\\round2\\KVContest-data-test-suite\\dataset_analyzer\\test_file.txt')
    main()
