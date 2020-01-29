from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from recordclass import recordclass
from src.common import storage, Ptw

# end - how many H lines had this index as the last one
# key_existed - number of cases key at the index existed at the time of hashload
# key_null - ...key didn't exist
HCases = recordclass('HCases', 'end, key_existed, key_null')

class HashloadInfo:
    def __init__(self):
        # {key index in line: HCases}
        self.cases = defaultdict(lambda: HCases(0, 0, 0))
        self.wtab = None
    def comp_H(self, line):
        self.cases[len(line.key) - 1].end += 1
        for idx, key in enumerate(line.key):
            if storage[key]:
                self.cases[idx].key_existed += 1
            else:
                self.cases[idx].key_null += 1
    def _create_wtab(self):
        if self.wtab is not None:
            return
        self.wtab = Ptw(PrettyTable([
            'Key index', 'Existed', "Didn't exist", 'Last key'
        ]), 0, ['c', 'R'])
        for idx in self.cases:
            h = self.cases[idx]
            self.wtab.write_raw([
                idx, h.key_existed, h.key_null, h.end
            ])
        self.wtab.add_raw_to_table()
    def output(self):
        self._create_wtab()
        return self.wtab.table
    def graph(self):
        self._create_wtab()
        # grouped bar chart
        labels, key_existed, key_null, last_key = [], [], [], []
        self.wtab.sort_raw()
        for row in self.wtab.raw_data:
            labels.append(row[0])
            key_existed.append(row[1])
            key_null.append(row[2])
            last_key.append(row[3])

        loc = np.arange(len(labels))
        width = 0.33

        fig, ax = plt.subplots()
        ax.bar(loc, key_existed, width/3, label='Key existed')
        ax.bar(loc + width/3, key_null, width/3, label="Key didn't exist")
        ax.bar(loc+ 2*(width/3), last_key, width/3, label='Key was last')

        ax.set_xlabel('Key index')
        ax.set_ylabel('Number of cases')
        ax.set_title('More about keys in hashload')
        ax.set_xticks(loc)
        ax.set_xticklabels(labels)
        ax.legend()

        fig.tight_layout()
        plt.show()
