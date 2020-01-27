class PrettyTableWrapper:
    def __init__(self, table, sortby=None, aligns=None):
        """Create PrettyTableWrapper.
        Args:
            table (PrettyTable).
            sortby (id: str or int | tuple(id, reversesort=bool)) opt: Sorts table by field name.
            aligns (list) opt: Align setting applied positionally on columns.
        """
        self.table = table
        self.n_columns = len(table.field_names)
        self.raw_data = []
        self.print_ptr = 0
        self.format_factories = {}

        if sortby is not None:
            if isinstance(sortby, tuple):
                table.sortby = sortby[0] if isinstance(sortby[0], str) else table.field_names[sortby[0]]
                table.reversesort = sortby[1]
            else:
                table.sortby = sortby if isinstance(sortby, str) else table.field_names[sortby]

        if aligns:
            for align, field in zip(aligns, table.field_names):
                table.align[field] = align

    def coalesce(self, row_data):
        """Coalesce missing fields with empty string.
        Args:
            row_data (list): Fields data.
        """
        for i in range(self.n_columns - len(row_data)):
            row_data.append('')
        return row_data

    def add_coalesce(self, row_data):
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
        self.raw_data.append(self.coalesce(row_data))

    def add_raw_to_table(self):
        for row in self.raw_data[self.print_ptr:]:
            self.table.add_row([
                self.format_factories[idx](cell)
                if idx in self.format_factories and 
                not cell == '' else cell
                for idx, cell in enumerate(row)
            ])
            # for idx in self.format_factories:
            #     # format non-empty cells
            #     if row[idx]:
            #         row[idx] = self.format_factories[idx](row[idx])
            # self.table.add_row(row)
        self.print_ptr = len(self.raw_data)
        