from collections import defaultdict
from recordclass import recordclass
from src.common import storage, Ptw, Bar

# end - how many H lines had this index as the last one
# key_existed - number of cases key at the index existed at the time of hashload
# key_null - ...key didn't exist
# min_len - length of shortest key on this index
# max_len - length of longest key on this index
HCases = recordclass('HCases', 'end, key_existed, key_null, min_len, max_len')

class HashloadInfo:
    """Computes statistics about hashload command only.
    Gets the number of keys in hashload,
    if individual keys existed in storage at the time of hashload or not,
    and also min and max length of a key in hashload."""
    def __init__(self):
        # {key index in line: HCases}
        self.cases = defaultdict(lambda: HCases(0, 0, 0, 99, 0))
        self.wtab = None
    def comp_H(self, line):
        self.cases[len(line.key) - 1].end += 1
        for idx, key in enumerate(line.key):
            h = self.cases[idx]
            if storage[key]:
                h.key_existed += 1
            else:
                h.key_null += 1
            l = len(key)
            if l < h.min_len:
                h.min_len = l
            if l > h.max_len:
                h.max_len = l
    def _create_wtab(self):
        if self.wtab is not None:
            return
        self.wtab = Ptw(field_names=[
            'Key index', 'Existed', "Didn't exist", 'Last key', 'Min len', 'Max len'
        ], sortby=0, aligns='cR')
        for idx in self.cases:
            h = self.cases[idx]
            self.wtab.write_raw([
                idx, h.key_existed, h.key_null, h.end, h.min_len, h.max_len
            ])
        self.wtab.add_raw_to_table()
    def output(self):
        self._create_wtab()
        return self.wtab.table
    def graph(self):
        self._create_wtab()
        self.wtab.sort_raw()
        Bar.chart(
            Bar.unpack(
                self.wtab.raw_data, from_idx=1, labels=[
                    'Key existed',
                    "Key didn't exist",
                    'Key was last',
                    'Shortest key length',
                    'Longest key length'
                ]
            ),
            title='More about keys in hashload',
            xlabel='Key index',
            ylabel='Number of cases',
            group_labels=[row[0] for row in self.wtab.raw_data]
        )
