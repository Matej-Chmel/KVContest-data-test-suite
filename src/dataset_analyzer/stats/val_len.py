from collections import defaultdict
from src.common import Line, Ptw, storage
from src.common.graph import pie_chart

class ValueLengths:
    """Computes number of occurrences of length of a value."""    
    def __init__(self):
        # occurrences by length
        self.ocs = defaultdict(lambda: 0)
        self.wtab: Ptw = None
    def comp_A(self, line: Line):
        self.ocs[len(line.val) + len(storage[line.key])] += 1
    def comp_S(self, line: Line):
        self.ocs[len(line.val)] += 1
    def _create_wtab(self):
        if self.wtab is not None:
            return
        self.wtab = Ptw(
            ['Length', 'Occurrences'],
            sortby=1,
            reverse_sort=True,
            aligns='R'
        )
        for length in self.ocs:
            self.wtab.write_raw([length, self.ocs[length]])
        self.wtab.sort_raw()
        self.wtab.add_raw_to_table()
    def output(self):
        self._create_wtab()
        table_by_ocs = str(self.wtab.table)
        self.wtab.re_sort(0, False)
        return '\n'.join([table_by_ocs, str(self.wtab.table)])
    def graph_pie_chart(self):
        self._create_wtab()
        self.wtab.re_sort(0, False)
        pie_chart(
            self.ocs.values(),
            self.ocs.keys(),
            title='Occurrences of value lengths'
        )
