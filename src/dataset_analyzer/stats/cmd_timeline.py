from collections import defaultdict
import matplotlib.pyplot as plt
from recordclass import recordclass
from src.common import COMMANDS

# total_ocs - stores current total occurrences of command
# samples - list of samples of total_ocs taken at times of sampling
#   these are used as y-values on a graph
CmdSample = recordclass('CmdSample', 'total_ocs, samples')

class CommandTimeline:
    def __init__(self, lines_sample=500):
        """Args:
            lines_sample (int) opt: Splits graph into sections
                each containing this number of lines.
        """
        self.lines_sample = max([lines_sample, 1])
        self.next_sample = 1
        # {cmd: list of occurrences at the time}
        self.y_cmd = defaultdict(lambda: CmdSample(0, []))
        self.x_time = []
    def _create_sample(self, line_num):
        for cmd in COMMANDS:
            csample = self.y_cmd[cmd]
            csample.samples.append(csample.total_ocs)
        self.x_time.append(line_num)
    def comp_all_timeline(self, line):
        self.y_cmd[line.cmd].total_ocs += 1
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
        for cmd in self.y_cmd:
            plt.plot(self.x_time, self.y_cmd[cmd].samples, label=cmd)
        plt.xlabel('Line number')
        plt.ylabel('Number of occurrences')
        plt.title('Commands timeline')
        plt.legend()
        plt.show()
