from airtable import Airtable


class DataRouter:
    def __init__(self, base, table_name, api_key, assignee):
        self._base = base
        self._table_name = table_name
        self._api_key = api_key
        self._assignee = assignee

        self.airtable = Airtable(self._base, self._table_name,
                                 api_key=self._api_key)
        self.unfiltered_table = self.airtable.get_all()
        self.filtered_table = self.filter_by_assigned()

    def filter_by_assigned(self):
        """
        Filters Airtable.get_all() by assignee passed to Class
        """
        if self._assignee is None:
            print('Cannot filter. No assignee passed to class.')
            return None
        filtered_table = list()
        for row in self.airtable.get_all():
            if row['fields']['Editor']['name'] == self._assignee:
                filtered_table.append(row)
        return filtered_table

    def print_assigned(self, filtered=False):
        table = self.unfiltered_table
        if filtered is True:
            table = self.filtered_table

        for i in table:
            print(i)
            print("\n")