from collections import defaultdict
from inspect import signature
from src.common import COMMANDS

class Activator:
    def __init__(self, desired_stats=None):
        # {command: [statistics computation functions, ...]}
        # func names: comp_{CMDS}[_{any}]({one arg - line})
        self.active_stats = defaultdict(list)
        # [functions returning printable object]
        # names: output[_{any}]
        self.console_output = []
        # [functions showing matplot graph]
        # names: graph[_{any}]
        self.graph_output = []
        # [functions to be called after whole dataset was read]
        # names: end[_{any}]({one arg - last line})
        self.end_dataset = []
        # TODO: get dataset stat data for generator

        if desired_stats:
            self.activate(desired_stats)

    def _activate_one(self, bound, cmds):
        for cmd in cmds:
            self.active_stats[cmd].append(bound)

    def activate(self, desired_stats):
        """Extract bound functions from desired stats 
        to data structures in .stats module.
        Args:
            desired_stats (list) -> Item: Class or instance 
                of statistic you want to compute.
        """    
        for item in desired_stats:
            i_dir = item.__dir__()
            i_norm = list(attr for attr in i_dir if not attr.startswith('_'))
            for attr in i_norm:
                bound = getattr(item, attr, None)
                if callable(bound):
                    if attr.startswith('comp_') and len(signature(bound).parameters) == 1:
                        splits = attr.split('_', maxsplit=2)
                        if len(splits) == 1 or splits[1] == 'all':
                            # all cmds
                            self._activate_one(bound, COMMANDS)
                        else:
                            self._activate_one(bound, splits[1])
                    elif attr.startswith('output'):
                        self.console_output.append(bound)
                    elif attr.startswith('graph'):
                        self.graph_output.append(bound)
                    elif attr.startswith('end') and len(signature(bound).parameters) == 1:
                        self.end_dataset.append(bound)
