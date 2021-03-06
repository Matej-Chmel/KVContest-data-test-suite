from prettytable import PrettyTable

class PrettyTableWrapper:
    def __init__(
            self, field_names=None, 
            sortby=None, reverse_sort=False, 
            aligns=None, common_formatter=None
    ):
        """Create PrettyTableWrapper.
        Args:
            field_names (list).
            sortby (str or int) opt: Sorts table by column.
            reverse_sort (bool) opt.
            aligns (iterable) opt: Align setting applied positionally on columns.
                If last align is uppercase, then remaining columns will be aligned that way.
            common_formatter (tuple(idxs_sequence, function)) opt: 
                Add common formatter function to selected columns.
        """
        table = PrettyTable(field_names)
        self.table = table
        self.n_columns = len(field_names)
        self.raw_data = []
        self.print_ptr = 0
        self.sortby = sortby
        self.reverse_sort = reverse_sort
        self.format_factories = {}

        if sortby is not None:
            self._apply_sort(sortby, reverse_sort)

        if aligns and len(aligns) != 0: 
            if aligns[-1].isupper():
                table.align = aligns[-1].lower()
            for align, field in zip(aligns[:-1], table.field_names):
                table.align[field] = align

        if common_formatter:
            self.update_format_factories({
                idx:common_formatter[1]
                for idx in common_formatter[0]
            })

    def coalesce(self, row_data):
        """Coalesce missing fields with empty string.
        Args:
            row_data (list): Fields data for one ROW.
        """
        # pylint: disable=unused-variable
        for i in range(self.n_columns - len(row_data)):
            row_data.append('')
        return row_data

    def add_coalesce(self, row_data):
        """Adds ROW_data straight to PrettyTable.
        Great if you don't want to mess with raw data.
        Args:
            row_data (list): Fields data for one ROW.
        """   
        self.table.add_row(self.coalesce(row_data))

    def update_format_factories(self, factories):
        """Add format functions for row_data.
        Args:
            factories (dict): {column id: function}
        """
        for key in factories:
            if isinstance(key, str):
                factories[self.table.field_names.index(key)] = factories.pop(key)
        self.format_factories.update(factories)

    def write_raw(self, row_data):
        """Appends ROW data to raw_data list. This is saved in wrapper
        and is not added to the PrettyTable until self.add_raw_to_table() is called.
        Args:
            row_data (list): Fields data for one ROW.
        """        
        self.raw_data.append(self.coalesce(row_data))

    def add_raw_to_table(self):
        """Adds all yet not printed data from raw_data to PrettyTable.
        Raw_data stays in wrapper and is accessible as list.
        Every call to this method adds only data that hasn't been added yet with this method.
        """        
        for row in self.raw_data[self.print_ptr:]:
            self.table.add_row([
                self.format_factories[idx](cell)
                if idx in self.format_factories and 
                not cell == '' else cell
                for idx, cell in enumerate(row)
            ])
        self.print_ptr = len(self.raw_data)

    def _apply_sort(self, sortby, reverse_sort):
        self.table.sortby = sortby if isinstance(sortby, str) else self.table.field_names[sortby]
        self.sortby = self.table.field_names.index(self.table.sortby)
        self.reverse_sort = reverse_sort
        self.table.reversesort = self.reverse_sort

    def sort_raw(self):
        """Sorts raw_data based on self.sortby and self.reverse_sort.
        Doesn't sort PrettyTable itself.
        """        
        self.raw_data.sort(key=lambda item: item[self.sortby], reverse=self.reverse_sort)

    def re_sort(self, sortby, reverse_sort=False):
        """Resorts raw_data as well as PrettyTable itself.
        Args:
            sortby (int | str): Names of column to sort by or its index in self.table.field_names.
            reverse_sort (bool) opt: False = sort ascending, True = sort descending.
        """        
        self._apply_sort(sortby, reverse_sort)
        self.sort_raw()
        