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
        filtered_table = list()
        for row in self.unfiltered_table:
            try:
                if row['fields']['Editor']['name'] == self._assignee:
                    filtered_table.append(row)
            except KeyError:
                print('Blog with id #{} not assigned. Skipping...'
                      .format(row['id']))
        return filtered_table

    def print_assigned(self, filtered=True):
        table = self.filtered_table
        if filtered is False:
            table = self.unfiltered_table

        for i in table:
            print(i)
            print("\n")

    def temp_filter(self):
        matches = list()
        for row in self.filtered_table:
            asana_row = dict()
            asana_row['title'] = row['fields']['Post Title']
            asana_row['assignee'] = row['fields']['Editor']['name']
            try:
                asana_row['draft'] = row['fields']['Draft']
            except KeyError:
                asana_row['draft'] = ""
                print('Blog with id #{} has no Draft link.'
                      .format(row['id']))
            try:
                asana_row['issue'] = row['fields']['Issue']
            except KeyError:
                print('Blog with id #{} has no Issue link.'
                      .format(row['id']))
                asana_row['issue'] = ""
            matches.append(asana_row)
        return matches
