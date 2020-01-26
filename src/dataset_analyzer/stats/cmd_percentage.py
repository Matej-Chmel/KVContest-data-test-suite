from collections import defaultdict
from recordclass import recordclass
from prettytable import PrettyTable
from src.common import storage, percentage
from src.common.func import PrettyTableWrapper as Ptw

# stores number of cases 
# key was/was not found in storage when command was executed
CmdKeyCases = recordclass('CmdFound', 'key_existed, key_null')

class CommandPercentage:
    def __init__(self):
        self.cases = defaultdict(lambda: CmdKeyCases(0, 0))
        self.hashloads = 0
    def comp_ALRS(self, line):
        if storage[line.key]:
            self.cases[line.cmd].key_existed += 1
        else:
            self.cases[line.cmd].key_null += 1
    def comp_H(self, line):
        self.hashloads += 1
    def output(self):
        total = self.hashloads
        for key in self.cases:
            total += self.cases[key].key_existed + self.cases[key].key_null
        table = PrettyTable([
            'Command', 'Total occurrences', '% from total', 
            'Key existed', '% from ocs',
            "Key didn't exist", '% from ocs '
        ])
        table.align = 'r'
        wtab = Ptw(table, (1, True), ['c']) # sortby column, center first column
        for key in self.cases:
            key_existed = self.cases[key].key_existed
            key_null = self.cases[key].key_null
            ocs = key_existed + key_null
            table.add_row([
                key, ocs, percentage(ocs, total),
                key_existed, percentage(key_existed, ocs),
                key_null, percentage(key_null, ocs)
            ])
        wtab.add_row(['H', self.hashloads, percentage(self.hashloads, total)])
        return table
