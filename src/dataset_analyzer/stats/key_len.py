from collections import defaultdict
from src.common import Ptw
from src.common.math import percentage, percentage_str
from src.common.graph import pie_chart

def _create_wtab(self, wtab_name, ocs_dict, total):
    wtab = Ptw(
        ['Key length', 'Occurrences', '% from total'],
        sortby=1, reverse_sort=True, aligns='cR', common_formatter=((2, ), percentage_str)
    )
    for length in ocs_dict:
        ocs = ocs_dict[length]
        wtab.write_raw([
            length, ocs, percentage(ocs, total)
        ])
    wtab.add_raw_to_table()
    wtab.sort_raw()
    setattr(self, wtab_name, wtab)
def _graph_pie_chart(ocs_dict, title=''):
    pie_chart(ocs_dict.values(), ocs_dict.keys(), title=title)

class KeyLengths:
    """Computes number of occurrences of length of a key 
    in classic commands and also in hashload."""    
    def __init__(self):
        self.wtab_ALRS = None
        self.wtab_H = None
        # {key length: number of occurrences}
        self.key_len_ocs_ALRS = defaultdict(lambda: 0)
        self.key_len_ocs_H = defaultdict(lambda: 0)
        self.total_lines_ALRS = 0
        self.total_keys_H = 0
    def comp_ALRS(self, line):
        self.key_len_ocs_ALRS[len(line.key)] += 1
        self.total_lines_ALRS += 1
    def comp_H(self, line):
        for key in line.key:
            self.key_len_ocs_H[len(key)] += 1
            self.total_keys_H += 1
    def _create_all_wtabs(self):
        if self.wtab_ALRS is not None:
            return
        _create_wtab(self, 'wtab_ALRS', self.key_len_ocs_ALRS, self.total_lines_ALRS)
        _create_wtab(self, 'wtab_H', self.key_len_ocs_H, self.total_keys_H)
    def output(self):
        self._create_all_wtabs()
        return '\n'.join([
            '\nKey lengths in ALRS\n',
            str(self.wtab_ALRS.table),
            '\nKey lengths in Hashload\n',
            str(self.wtab_H.table)
        ])
    def graph_pie_chart(self):
        self._create_all_wtabs()
        _graph_pie_chart(self.key_len_ocs_ALRS, title='Key lengths in ALRS')
        _graph_pie_chart(self.key_len_ocs_H, title='Key lengths in Hashload')
