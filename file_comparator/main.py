from sys import argv
from os.path import dirname, realpath
from settings import MCHM_SETTINGS as g
from prompt import create_file_prompt

'''
Program that compares two files and outputs differences to another file.
'''

class MODES:
    # print to console first line that failed comparison
    STOP_AT_FAIL = 0
    # print all failed lines to console
    PRINT_ALL = 1
    # output all failed lines to file
    OUTPUT_ALL = 2
    #
    # variable
    mode = STOP_AT_FAIL

def set_mode():
    modes = {
        k:v for k, v in MODES.__dict__.items() 
        if not k.startswith('_') and k != 'mode'
    }
    allowed_input = {}
    print('Choose mode:')
    for mode_name in modes:
        print('{} | {}'.format(mode_name, modes[mode_name]))

        # accept:
        # full mode name
        allowed_input[mode_name.lower()] = mode_name
        # first word of mode name
        allowed_input[mode_name.split('_', 1)[0].lower()] = mode_name
        # number value that mode represents
        allowed_input[str(MODES.__dict__[mode_name])] = mode_name

    selected = input('>>> ').lower()
    if selected in allowed_input:
        accepted = allowed_input[selected]
        MODES.mode = MODES.__dict__[accepted]
        print('You selected: {}'.format(accepted))
        return
    print('Mode stays at default.')
    
# print format

def get_failed_format(order, one, two):
    return [
        '1 | {}: {}'.format(order, one),
        '2 | {}: {}'.format(order, two)
    ]

# comparator function based on mode
# returns False if iteration should stop

def stop_at_fail(order, one, two):
    if one != two:
        print('\n'.join(get_failed_format(order, one, two)) + '\n')
        return False
    return True

def print_all(order, one, two):
    stop_at_fail(order, one, two)
    return True

# list of failed comparisons
output = []

def output_all(order, one, two):
    if one != two:
        failed_tuple = get_failed_format(order, one, two)
        for line in failed_tuple:
            output.append(line)
        output.append('')
    return True

ptr_comparators = (
    stop_at_fail,
    print_all,
    output_all
)

def compare_lines(order, one, two):
    return ptr_comparators[MODES.mode](order, one, two)

# driver
def main():
    g.setOptions(BASE_DIR=dirname(realpath(__file__)))
    if len(argv) != 3:
        print('Two files have to be dropped onto the script.')
        print('Bad args: {}'.format(str(argv)))
        return
    set_mode()
    with open(argv[1]) as file1:
        with open(argv[2]) as file2:
            i = 1
            for line1, line2 in zip(file1, file2):
                if not compare_lines(i, line1.rstrip('\n'), line2.rstrip('\n')):
                    break
                i += 1
    if MODES.mode == MODES.OUTPUT_ALL:
        for i in range(min([len(output), 14])):
            print(output[i])
        print('...')
        create_file_prompt(
            'Do you want to save differences to file?',
            output,
            'txt'
        )

if __name__ == "__main__":
    main()
