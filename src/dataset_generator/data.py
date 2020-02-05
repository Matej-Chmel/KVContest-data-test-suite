from dataclasses import dataclass
from itertools import cycle
from random import choice as rchoice, randint
from string import ascii_letters, digits
from numpy.random import choice as nchoice
from src.common import storage

@dataclass
class MinMax:
    """min, max inclusive struct"""
    min: int = 0
    max: int = 99
    def range(self, dmin=0, dmax=1):
        return range(self.min + dmin, self.max + dmax)
    def it(self, dmin=0, dmax=1):
        return iter(self.range(dmin, dmax))
    def __iter__(self):
        return iter(self.range())

@dataclass
class Dataset:
    cmds: list = None
    weights: list = None
    cycles_cmds: list = None
    zones: list = None

small = Dataset()
medium_H = Dataset()
medium_AH = Dataset()
datasets = {
    'L R S': small,
    'H L R S': medium_H,
    'A H L R S': medium_AH
}

key_len = MinMax(5, 9)
value_len = MinMax(62, 150)
append_len = MinMax(17, 39)
hashload_len = MinMax(10, 99)

rnd_limit = 300
def get_rnd_cycle(source, size=rnd_limit, weights=None):
    return cycle(nchoice(source if isinstance(source, list) else list(source), size=size, p=weights))

cyc_val_len = get_rnd_cycle(value_len.range())
cyc_A_len = get_rnd_cycle(append_len.range())
cyc_H_len = get_rnd_cycle(hashload_len.range())

SMALL_COMMANDS = 'LRS'
# tuple (command letter, bool: execute on NEW key)
small.cmds = [(cmd, key_state) for cmd in SMALL_COMMANDS for key_state in (True, False)]
medium_H.cmds = small.cmds + [('H', )]
medium_AH.cmds = small.cmds + [('A', True), ('A', False), ('H', )]

def get_weights(orig_weights: list):
    """Changes orig_weights to probability total=1 format and
    returns it with last value.
    Args:
        orig_weights (list): Weights without last value in total=100 format.
    Returns:
        list
    """
    orig_weights = [item/100 for item in orig_weights]
    orig_weights.append(1 - sum(orig_weights))
    return orig_weights

cyc_key_is_new = get_rnd_cycle([True, False], weights=get_weights([1]))

# weight is list of lists of probabilites for zones

# s [('L', True), ('L', False), ('R', True), ('R', False), ('S', True), ('S', False)]
small.weights = [get_weights([2, 28, 1, 19, 48])]
# mH [('L', True), ('L', False), ('R', True), ('R', False), ('S', True), ('S', False), ('H',)]
medium_H.weights = [
    get_weights([0.2, 1.25, 0, 16.75, 75.40, 0.25]),
    get_weights([0.2, 1.25, 0, 12.15, 56.95, 0.25]),
    get_weights([0.2, 1.25, 0, 5.75, 20.70, 0.25])
]
# mAH [('L', True), ('L', False), ('R', True), ('R', False), ('S', True), ('S', False),
# ('A', True), ('A', False), ('H',)]
medium_AH.weights = [
    get_weights([0.15, 1.1, 0, 16.6, 75.25, 0.1, 0, 1.3]),
    get_weights([0.15, 1.1, 0, 12, 56.75, 0.1, 0, 1.3]),
    get_weights([0.15, 1.1, 0, 5.6, 20.40, 0.1, 0, 1.15])
]

def generate_cmds(dataset: Dataset):
    dataset.cycles_cmds = []
    for weight in dataset.weights:
        rnd_idxs = nchoice(range(len(dataset.cmds)), size=rnd_limit * 10, p=weight)
        source = [dataset.cmds[idx] for idx in rnd_idxs]
        dataset.cycles_cmds.append(
            cycle(source)
        )

key_chars = list(ascii_letters + digits)
key_lengths = get_rnd_cycle(key_len.range())

def new_key_generator():
    """Generator of new keys.
    Yields: str
    """
    def _rnd_key():
        return ''.join(nchoice(key_chars, size=next(key_lengths)))
    while True:
        key = _rnd_key()
        while key in storage:
            key = _rnd_key()
        yield key

def existing_key():
    if len(storage) == 0:
        raise KeyError
    return rchoice(list(storage))

def existing_key_else_new():
    try:
        return existing_key()
    except KeyError:
        return next(new_key_generator())

value_chars = list(ascii_letters)

def rnd_word(length: int):
    return ''.join(nchoice(value_chars, size=length))

word_len = MinMax(1, 15)
words = [
    None,
    get_rnd_cycle(ascii_letters),
    *[
        cycle([
            rnd_word(l) for i in range(rnd_limit)
        ])
        for l in word_len.it(1, 1)
    ]
]

def rnd_value(length: int):
    value = ''
    while (n := len(value)) != length:
        value += next(words[randint(1, min([word_len.max, length - n]))])
        if len(value) != length:
            value += ' '
    return value

def _get_zones(*milestones):
    end = milestones[-1]
    return tuple(m / end for m in milestones)

small.zones = _get_zones(1)
medium_H.zones = _get_zones(32000, 130000, 1300500)
medium_AH.zones = _get_zones(23000, 105500, 1300500)

def create_zones(total_lines: int, dataset: Dataset):
    dataset.zones = tuple(int(m * total_lines) for m in dataset.zones)

if __name__ == "__main__":
    print(small.zones, medium_H.zones, sep='\n\n')
    create_zones(10001, small)
    create_zones(1300500, medium_H)
    print(small.zones, medium_H.zones, sep='\n\n')
