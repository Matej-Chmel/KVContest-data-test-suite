from collections import defaultdict
from statistics import median
from src.common import Line, Ptw, storage

class ValueLengthToAppendRelations:
    """Computes relation between value length and
    probability that to that value will be appended another one."""
    def __init__(self):
        # {value length: times appended to}
        self.pre_append_lengths = defaultdict(lambda: 0)
        # {lengths of appended values}
        self.append_lengths = []
        # {value: times appended to}
        self.values = defaultdict(lambda: 0)
    def comp_A(self, line: Line):
        self.pre_append_lengths[len(storage[line.key])] += 1
        self.values[line.val] += 1
        self.append_lengths.append(len(line.val))
    def output(self):
        tlen = Ptw(
            ['Length', 'Appended to'],
            sortby=0, aligns='R'
        )
        for length in self.pre_append_lengths:
            tlen.add_coalesce([length, self.pre_append_lengths[length]])
        tmed = Ptw(
            ['Subject', 'Value'],
            aligns='cR'
        )
        tmed_rows = [
            [
                'Median of how many times was appended to single value',
                median(self.values.values())
            ],
            ['Minimum appended length', min(self.append_lengths)],
            ['Median of appended value length', median(self.append_lengths)],
            ['Maximum appended length', max(self.append_lengths)],
        ]
        for row in tmed_rows:
            tmed.add_coalesce(row)
        return '\n\n'.join([str(tlen.table), str(tmed.table)])
