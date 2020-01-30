from collections import defaultdict
from recordclass import recordclass
from src.common import storage, Ptw, Bar, extract_sublist
from src.common.math import percentage, percentage_str

# stores number of cases 
# key was/was not found in storage when command was executed
CmdKeyCases = recordclass('CmdFound', 'key_existed, key_null')

class CommandPercentage:
    def __init__(self):
        # {cmd: CmdKeyCases}
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
        if self.wtab is not None:
            return
        total = self.hashloads
        for key in self.cases:
            total += self.cases[key].key_existed + self.cases[key].key_null
        # sortby ocs, max first, center first column, rest align to right
        self.wtab = Ptw(field_names=[
            'Command', 'Total occurrences', '% from total', 
            'Key existed', '% from ocs',
            "Key didn't exist", '% from ocs '
        ], sortby=1, reverse_sort=True, aligns=['c', 'R'], 
                        common_formatter=([2, 4, 6], percentage_str))
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
        self._create_wtab()
        return self.wtab.table
    def graph(self):
        self._create_wtab()
        self.wtab.sort_raw()
        Bar.chart(
            Bar(
                upper=extract_sublist(self.wtab.raw_data, 5, 0),
                upper_label="Key didn't exist",
                bottom=extract_sublist(self.wtab.raw_data, 3, 0),
                bottom_label='Key existed',
                same_loc=Bar(
                    upper=[row[1] if row[0] == 'H' else 0 for row in self.wtab.raw_data],
                    upper_label='Hashload occurences',
                )
            ),
            title='Command Percentage',
            xlabel='Commands',
            ylabel='Number of cases',
            group_labels=[row[0] for row in self.wtab.raw_data],
            width=0.35
        )
