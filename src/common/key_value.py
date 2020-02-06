from collections import defaultdict
from typing import Union

class Line:
    def __init__(self, line_num, line_splits):
        self.num = line_num
        self.cmd = line_splits[0]
        self.key = line_splits[1:] if self.cmd == 'H' else line_splits[1]
        self.val = line_splits[2] if self.cmd in 'AS' else None

# dict representing key-value storage
storage = defaultdict(lambda: '')
# for hashloads use dict without default value
strict_storage = {}

def execute_line_no_loads(line: Line):
    if line.cmd == 'A':
        storage[line.key] += line.val
    elif line.cmd == 'R':
        if line.key in storage:
            del storage[line.key]
    elif line.cmd == 'S':
        storage[line.key] = line.val

def hash_value(val: str) -> int:
    h = 5381
    length = len(val)
    for c in val:
        # add hash of character and simulate int64 overflow
        h = ((h * 33) + ord(c) * length) & ((1 << 64) - 1)
    return h

def hash_load(keys: list) -> int:
    h = 0
    for key in keys:
        if key in strict_storage:
            # xor hash of value and simulate int64 overflow
            h = (h ^ hash_value(strict_storage[key])) & ((1 << 64) - 1)
    try:
        return h % len(strict_storage)
    except ZeroDivisionError:
        # There is nothing like that in the original solution,
        # there might be a guarantee that always len(storage) > 0
        return 0

def execute_line_return_result(line: Line) -> Union[str, None]:
    if line.cmd == 'H':
        return str(hash_load(line.key))
    if line.cmd == 'S':
        strict_storage[line.key] = line.val
    elif line.cmd == 'R':
        if line.key in strict_storage:
            del strict_storage[line.key]
    elif line.cmd == 'A':
        if line.key in strict_storage:
            strict_storage[line.key] += line.val
        else:
            strict_storage[line.key] = line.val
    elif line.cmd == 'L':
        if line.key in strict_storage:
            return strict_storage[line.key]
        return 'null'
