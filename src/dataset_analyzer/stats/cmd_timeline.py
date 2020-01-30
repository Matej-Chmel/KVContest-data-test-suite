from collections import defaultdict
import matplotlib.pyplot as plt
from src.common import CASUAL_COMMANDS
from src.dataset_analyzer.stats import CommandPercentage

class CommandTimeline:
    def __init__(self, cmdPercentageObject=CommandPercentage(), lines_sample=500):
        """
        Args:
            cmdPercentageObject (CommandPercentage) opt:
                CommandPercentage stat is required for thisone to be computed.
            lines_sample (int) opt: Splits graph into sections
                each containing this number of lines.
        """
        self.CP = cmdPercentageObject
        self.lines_sample = max([lines_sample, 1])
        self.next_sample = 1
        # {cmd: list of occurrences at the time}
        self.samples = defaultdict(list)
        self.x_time = []
    def _create_sample(self, line_num):
        for cmd in CASUAL_COMMANDS:
            ccases = self.CP.cases[cmd]
            self.samples[cmd].append(ccases.key_existed + ccases.key_null)
        self.samples['H'].append(self.CP.hashloads)
        self.x_time.append(line_num)
    def comp_all_timeline(self, line):
        if line.num == self.next_sample:
            self._create_sample(line.num)
            self.next_sample += self.lines_sample
    def end_of_dataset(self, last_line):
        if last_line is None:
            return
        if self.x_time[-1] == last_line.num:
            return
        self._create_sample(last_line.num)
    def graph(self):
        for cmd in self.samples:
            plt.plot(self.x_time, self.samples[cmd], label=cmd)
        plt.xlabel('Line number')
        plt.ylabel('Number of occurrences')
        plt.title('Commands timeline')
        plt.legend()
        plt.show()
