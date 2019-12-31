# key value contest dataset generator
from random import choice, randint
from string import ascii_letters, digits
from os.path import isfile, dirname, realpath

# directory of main.py
BASE_DIR = dirname(realpath(__file__))

storage = {}
# list of rows
dataset = []
solution = []
# words = list of words
with open('words.txt') as f:
    words = [line.rstrip('\n') for line in f]

# datafile = fstream
def write_file_from_lines(filename, ext, lines):
    filename += '.{}'.format(ext)
    fullname = '{0}/{1}'.format(BASE_DIR, filename)
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

'''
what can happen:
    S   - save new key
        - overwrite value
    L   - load existing key
        - load non-existing key
    R   - remove existing key
        - remove non-existing key
'''

# generators

def generate_key():
    return ''.join(choice(ascii_letters + digits) for i in range(randint(5, 10)))

def unique_key():
    key = generate_key()
    # such key already exists
    while key in storage:
        key = generate_key()
    return key

def generate_value():
    return ' '.join(choice(words) for i in range(randint(1, 4)))

# cases

def save_new_key():
    key = unique_key()
    value = generate_value()
    storage[key] = value
    dataset.append(' '.join(['S', key, value]))

def overwrite_key():
    # keys empty
    if len(storage) == 0:
        save_new_key()
    else:
        key = choice(list(storage))
        value = generate_value()
        storage[key] = value
        dataset.append(' '.join(['S', key, value]))

def load_existing():
    if len(storage) == 0:
        load_null()
    else:
        key = choice(list(storage))
        dataset.append(' '.join(['L', key]))
        solution.append(storage[key])

def load_null():
    dataset.append(' '.join(['L', unique_key()]))
    solution.append('null')

def remove_existing():
    if len(storage) == 0:
        remove_null()
    else:
        key = choice(list(storage))
        del storage[key]
        dataset.append(' '.join(['R', key]))

def remove_null():
    dataset.append(' '.join(['R', unique_key()]))

# weighted list of function pointers
ptr_cases = [save_new_key] * 18 + [overwrite_key] * 15 + [load_existing] * 33 + [load_null] * 9 + [remove_existing] * 20 + [remove_null] * 5

# dataset logic
def add_row():
    choice(ptr_cases)()

# input logic

def yes_no(prompt=''):
    if prompt:
        print(prompt)
    answer = input('>>> ')
    if answer.lower() in ['y', 'yes', 'ok', '']:
        return True
    if answer.lower() in ['n', 'no']:
        return False
    print('Please, answer \'yes\' or \'no\'.')
    return yes_no()

def file_logic(prompt, ext, lines):
    if yes_no(prompt):
        if not write_file_from_lines(input('Name: '), ext, lines):
            return file_logic(prompt, ext, lines)
        else:
            return True
    else:
        return False

# driver code
def main():
    print('Welcome to dataset generator for KV contest.')
    for i in range(int(input('Enter number of rows: '))):
        if i % 10000 == 0:
            print(i)
        add_row()
    print('Generated:')
    for i in range(min([len(dataset), 100])):
        print(dataset[i])
    print('...')
    if file_logic('Save dataset to file?', 'txt', dataset):
        file_logic('Save solution to file?', 'txt', solution)
    print('Exiting.')

if __name__ == "__main__":
    main()
