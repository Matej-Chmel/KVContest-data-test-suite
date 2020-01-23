from collections import defaultdict
from recordclass import recordclass
from prettytable import PrettyTable

class Line:
    def __init__(self, line_num, line_splits):
        self.num = line_num
        self.cmd = line_splits[0]
        self.key = line_splits[1]
        if len(line_splits) == 3:
            self.val = line_splits[2]
        else:
            self.val = None

class STATS:
    @staticmethod
    def get_output():
        return 'Not implemented'
    @staticmethod
    def graph():
        raise NotImplementedError

class ALRS(STATS):
    """
    Derived classes can compute stats from lines
    starting with commands A, L, R or S.
    """
    @staticmethod
    def compute_alsr(line):
        """Compute and add stats from line to already computed once.
        Args:
            line (Line): Object representation of line string.
        """             
        raise NotImplementedError
    
class H(STATS):
    """Computes only hashload (H) command."""
    @staticmethod
    def compute_h(line):
        raise NotImplementedError

# dict representing key-value storage
storage = defaultdict(lambda: '')

def execute_line(line):
    if line.cmd == 'A':
        storage[line.key] += line.val
    elif line.cmd == 'L':
        # load
        pass
    elif line.cmd == 'R':
        del storage[line.key]
    elif line.cmd == 'S':
        storage[line.key] = line.val
    else: #H
        # hashload
        pass

# stores number of cases key was/was not found in storage when command was executed
CmdKeyCases = recordclass('CmdFound', 'key_existed, key_null')

class CommandPercentage(ALRS, H):
    cases = defaultdict(lambda: CmdKeyCases(0, 0))
    hashloads = 0
    cmds_processed = 0
    @staticmethod
    def compute_alsr(line):
        if storage[line.key]:
            CommandPercentage.cases[line.cmd].key_existed += 1
        else:
            CommandPercentage.cases[line.cmd].key_null += 1
        CommandPercentage.cmds_processed += 1
    @staticmethod
    def compute_h(line):
        CommandPercentage.hashloads += 1
        CommandPercentage.cmds_processed += 1
    @staticmethod
    def _get_cmd_table_row(cmd):
        key_existed = CommandPercentage.cases[cmd].key_existed
        key_null = CommandPercentage.cases[cmd].key_null
        ocs = key_existed + key_null
        total = CommandPercentage.cmds_processed
        return [
            cmd,
            ocs, (ocs / total) * 100,
            key_existed, (key_existed / total) * 100,
            key_null, (key_null / total) * 100
        ]
    @staticmethod
    def get_output():
        table = PrettyTable([
            'Command', 'Total occurrences', 'Percentage0', 
            'Key existed', 'Percentage1',
            "Key didn't exist", 'Percentage2'
        ])
        for item in 'ALRS':
            table.add_row(CommandPercentage._get_cmd_table_row(item))
        table.add_row([
            'H',
            CommandPercentage.hashloads, (CommandPercentage.hashloads / CommandPercentage.cmds_processed) * 100,
            '', '', '', ''
        ])
        return table
