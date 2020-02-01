from statistics import median
from typing import Dict
from recordclass import RecordClass
from tqdm import tqdm_gui
from src.common import Bar, Line, Ptw

class KeyRecord(RecordClass):
    last_mention: int
    distances: list
    is_deleted: bool = False
    set_after_del: bool = False

class KeyDistances:
    """Computes median of distance between key mentions, 
    median of number of unique keys per hashload, ..."""
    # pylint: disable=no-value-for-parameter
    def __init__(self):
        self.records: Dict[str, KeyRecord] = {}
        self.wtab = None
        self.results: Dict[str, object] = None
        self.H_list_lengths = []
        self.H_set_lengths = []
    def _existing_key(self, key, line_num):
        record = self.records[key]
        record.distances.append(line_num - record.last_mention)
        record.last_mention = line_num
        return record
    def comp_ALRS(self, line: Line):
        if line.key in self.records:
            record = self._existing_key(line.key, line.num)
            if not record.set_after_del:
                if not record.is_deleted:
                    if line.cmd == 'R':
                        record.is_deleted = True
                else:
                    if line.cmd in 'AS':
                        record.set_after_del = True
        else:
            self.records[line.key] = KeyRecord(last_mention=line.num, distances=[])
    def comp_H(self, line: Line):
        self.H_list_lengths.append(len(line.key))
        H_set = set(line.key)
        self.H_set_lengths.append(len(H_set))
        for key in H_set:
            if key in self.records:
                self._existing_key(key, line.num)
            else:
                self.records[key] = KeyRecord(last_mention=line.num, distances=[])
    def end_of_dataset(self, last_line):
        total_keys, keys_one_mention, keys_set_after_del = 0, 0, 0
        distances_medians, distances_lengths = [], []

        progress_bar = tqdm_gui(
            desc='Computing medians',
            total=len(self.records) + 4,
            position=0,
            leave=False
        )
        
        for key in self.records:
            record = self.records[key]
            total_keys += 1
            distances_lengths.append(len(record.distances) + 1)
            if record.set_after_del:
                keys_set_after_del += 1
            if record.distances:
                distances_medians.append(median(record.distances))
            else:
                keys_one_mention += 1
            progress_bar.update()
        
        def _median(source: list):
            m = median(source) if source else 0
            progress_bar.update()
            return m

        self.wtab = Ptw(['Subject', 'Value'], aligns='cR')
        self.results = {
            'Total number of keys': total_keys,
            'Keys seen once only': keys_one_mention,
            'Keys set after removing': keys_set_after_del,
            'Median of distances': _median(distances_medians),
            'Median of number of cmds per key': _median(distances_lengths),
            'Median of number of keys per hashload': _median(self.H_list_lengths),
            'Median of number of unique keys per hashload': _median(self.H_set_lengths)
        }
        for subject in self.results:
            self.wtab.write_raw([subject, self.results[subject]])
        self.wtab.add_raw_to_table()
        progress_bar.close()
    def output(self):
        return self.wtab.table
    def graph(self):
        Bar.chart(
            Bar.unpack([list(self.results.values())[:2]], labels=list(self.results.keys())[:2]),
            title='Key distances'
        )
