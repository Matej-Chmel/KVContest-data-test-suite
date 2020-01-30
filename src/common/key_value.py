from collections import defaultdict

class Line:
    def __init__(self, line_num, line_splits):
        self.num = line_num
        self.cmd = line_splits[0]
        self.key = line_splits[1:] if self.cmd == 'H' else line_splits[1]
        self.val = line_splits[2] if self.cmd in 'AS' else None

# dict representing key-value storage
storage = defaultdict(lambda: '')

def execute_line_no_loads(line):
    if line.cmd == 'A':
        storage[line.key] += line.val
    elif line.cmd == 'R':
        if line.key in storage:
            del storage[line.key]
    elif line.cmd == 'S':
        storage[line.key] = line.val

# TODO: output, loads for sol gen
