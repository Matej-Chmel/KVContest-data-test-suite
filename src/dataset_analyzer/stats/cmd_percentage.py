from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
from recordclass import recordclass
from src.common import storage, Ptw
from src.common.math import percentage, percentage_str

# stores number of cases 
# key was/was not found in storage when command was executed
CmdKeyCases = recordclass('CmdFound', 'key_existed, key_null')

class CommandPercentage:
    def __init__(self):
        self.cases = defaultdict(lambda: CmdKeyCases(0, 0))
        self.hashloads = 0
        self.wtab = None
    def comp_ALRS(self, line):
        if storage[line.key]:
            self.cases[line.cmd].key_existed += 1
        else:
            self.cases[line.cmd].key_null += 1
    def comp_H(self, line):
        self.hashloads += 1
    def _create_wtab(self):
        total = self.hashloads
        for key in self.cases:
            total += self.cases[key].key_existed + self.cases[key].key_null
        table = PrettyTable([
            'Command', 'Total occurrences', '% from total', 
            'Key existed', '% from ocs',
            "Key didn't exist", '% from ocs '
        ])
        table.align = 'r'
        self.wtab = Ptw(table, (1, True), ['c']) # sortby column, center first column
        self.wtab.update_format_factories({
            k:percentage_str for k in ['% from total', '% from ocs', '% from ocs ']
        })
        for key in self.cases:
            key_existed = self.cases[key].key_existed
            key_null = self.cases[key].key_null
            ocs = key_existed + key_null
            self.wtab.write_raw([
                key, ocs, percentage(ocs, total),
                key_existed, percentage(key_existed, ocs),
                key_null, percentage(key_null, ocs)
            ])
        self.wtab.write_raw(['H', self.hashloads, percentage(self.hashloads, total)])
        self.wtab.add_raw_to_table()
    def output(self):
        if self.wtab is None: self._create_wtab()
        return self.wtab.table
    def graph(self):
        if self.wtab is None: self._create_wtab()
        
        # bar chart
        N = len(self.wtab.raw_data)
        key_existed = [row[3] if not row[3] == '' else 0 for row in self.wtab.raw_data]
        key_null = [row[5] if not row[5] == '' else 0 for row in self.wtab.raw_data]
        hashload_ocs = [row[1] if row[3] == '' else 0 for row in self.wtab.raw_data]
        ind = np.arange(N)
        width = 0.35

        p1 = plt.bar(ind, key_existed, width)
        p2 = plt.bar(ind, key_null, width, bottom=key_existed)
        p3 = plt.bar(ind, hashload_ocs, width)
        
        plt.ylabel('Number of cases')
        plt.title('Command Percentage')
        plt.xticks(ind, [row[0] for row in self.wtab.raw_data])
        plt.legend((p1[0], p2[0], p3[0]), ('Key existed', "Key didn't exist", 'Hashload occurences'))

        plt.show()
