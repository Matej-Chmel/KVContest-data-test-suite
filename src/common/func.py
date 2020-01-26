class PrettyTableWrapper:
    def __init__(self, table, sortby=None, aligns=None):
        """Create PrettyTableWrapper.
        Args:
            table (PrettyTable).
            sortby (str or index) opt: Sorts table by field name.
            aligns (list) opt: Align setting applied positionally on columns.
        """
        self.table = table
        self.n_columns = len(table.field_names)

        if sortby is not None:
            if isinstance(sortby, tuple):
                table.sortby = sortby[0] if isinstance(sortby[0], str) else table.field_names[sortby[0]]
                table.reversesort = sortby[1]
            else:
                table.sortby = sortby if isinstance(sortby, str) else table.field_names[sortby]

        if aligns:
            for align, field in zip(aligns, table.field_names):
                table.align[field] = align

    def add_row(self, data):
        """Add row to table, coalesce missing fields with empty string.
        Args:
            data (list): Field data.
        """
        for i in range(self.n_columns - len(data)):
            data.append('')
        self.table.add_row(data)
        