from itertools import zip_longest
import matplotlib.pyplot as plt
import numpy as np

def extract_sublist(source, idx, default=0):
    """Return list from elements at idx for each sublist in source
    or default if such element is empty string.
    Args:
        source (list): List of sublists.
        idx (int): Element index.
    """
    return [sublist[idx] if sublist[idx] != '' else default for sublist in source]

class Bar:
    """Args:
        upper (list): Main data for bars.
        upper_label (str) opt: Bars label.
        bottom (list) opt: Bottom part data.
        same_loc (Bar) opt: Bars plotted on same location.
    """
    def __init__(
            self, upper=None, upper_label='', bottom=None, bottom_label='', same_loc=None
    ):                  
        self.upper = upper
        self.label = upper_label
        self.bottom = bottom
        self.blabel = bottom_label
        self.same_loc = same_loc
    def plot(self, ax, loc, width):
        if self.bottom:
            ax.bar(loc, self.bottom, width, label=self.blabel)
        ax.bar(loc, self.upper, width, bottom=self.bottom, label=self.label)
        if self.same_loc:
            self.same_loc.plot(ax, loc, width)
    @staticmethod
    def chart(
            data, title='', xlabel='', ylabel='', group_labels=None,
            width=0.5
    ):
        """
        Args:
            data (list): List of Bars or single Bar.
                --- Item (tuple | Bar): initializes Bar object.
            title (str) opt: Title graph.
            xlabel (str) opt: Label x axis.
            ylabel (str) opt: Label y axis.
            group_labels (list) opt: Label each group.
            width (float) opt: Width of a group.
        """
        if not isinstance(data, list):
            data = [data]
        loc = np.arange(
            len(data[0].upper)
            if isinstance(data[0], Bar)
            else len(data[0][0])
        )
        bars = len(data)
        swidth = width/bars
        fig, ax = plt.subplots()

        for idx, item in enumerate(data):
            if isinstance(item, Bar):
                item.plot(ax, loc + (idx*swidth - ((bars - 1)/2)*(width/bars)), swidth)
            else:
                Bar(*item).plot(ax, loc + (idx*swidth - ((bars - 1)/2)*(width/bars)), swidth)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(loc)
        if group_labels:
            ax.set_xticklabels(group_labels)
        ax.legend()

        fig.tight_layout()
        plt.show()
    @staticmethod
    def unpack(source, from_idx=0, labels=None):
        """
        Args:
            source (list of lists): Data.
            from_idx (int): Start index of each sublist.
            labels (list | int): Labels for bars.
                If int, idx of sublist items where labels are located in source.
        Returns:
            list: List of Bar objects.
                If used inside list, 
                please unpack return value of this method with *.
        """
        if isinstance(labels, int):
            labels = [sublist[labels] for sublist in source]
        def _bar_generator():
            for upper, label in zip_longest(list(zip(*source))[from_idx:], labels):
                yield Bar(upper, label)
        return list(_bar_generator())

def pie_chart(data, labels, explode=None, title='', shadow=True, start_angle=90):
    fig, ax = plt.subplots()
    ax.pie(
        data, labels=labels, explode=explode,
        autopct='%1.1f%%', shadow=shadow, startangle=start_angle
    )
    ax.axis('equal')
    ax.set_title(title)

    fig.tight_layout()
    plt.show()

### demos ###

def _bar1():
    Bar.chart(
        [
            ([1, 2, 3], '1 A', [4, 5, 6], '1 B'),
            ([7, 8, 9], '2'),
            Bar(
                [10, 1, 0], '3 A', [4, 5, 0], '3 B',
                Bar(
                    [0, 0, 8], '3 Replacement'
                )
            )
        ],
        title='Bar chart demo',
        xlabel='X axis, groups',
        ylabel='Y axis, values',
        group_labels=['ABC', 'DEF', 'GHI'],
        width=0.33
    )
def _bar2():
    Bar.chart(
        [
            *Bar.unpack(
                [
                    [1, 2, 3],
                    [1, 2, 3],
                    [1, 2, 3]
                ], labels=['Label One']
            )
        ]
    )
def _bar3():
    Bar.chart(
        Bar.unpack(
            [
                ['A', 1, 7],
                ['B', 3, 5]
            ], from_idx=1, labels=0
        )
    )
def _single_bar():
    Bar.chart(Bar([1, 2, 3], 'One'))

def _pie1():
    pie_chart(
        [10, 20, 30, 40],
        'ABCD',
        title='Pie chart ABCD 001'
    )

if __name__ == "__main__":
    # _bar1()
    # _bar2()
    # _bar3()
    # _single_bar()
    _pie1()
