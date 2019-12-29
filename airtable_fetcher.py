class TableFetcher:
    def __init__(self, airtable, assignee, last_fetched):
        """
        Takes an Airtable object and
        :param airtable:
        :param assignee:
        :param last_fetched:
        """
        self._assignee = assignee
        self._last_fetched = last_fetched
        self._airtable = airtable
        self._filtered_table = []

    def get_matches(self, field_name, sub_field=None):
        """
        Filters Airtable.get_all() by assignee passed to Class
        """
        # filtered_table = list()
        print('GETTING matches with createdTime later than {}'.format(
            self._last_fetched))
        for row in self._airtable.get_all():
            if row['createdTime'] > self._last_fetched:
                try:
                    if sub_field and row['fields'][field_name][sub_field] == \
                            self._assignee:
                        self._filtered_table.append(row)
                    elif row['fields'][field_name] == self._assignee:
                        self._filtered_table.append(row)
                except KeyError:  # blog not assigned
                    print('Blog with id #{} not assigned. Skipping...'.format(
                        row['id']))

    def print_matches(self, asana_preview=False):
        table = self._filtered_table
        if asana_preview:
            table = self.prep_matches()
        for i in table:
            print(i)
            print("\n")

    def prep_matches(self, match_structure):
        if not self._filtered_table:
            return -1
        matches = list()
        for row in self._filtered_table:
            match_row = dict()
            match_row['title'] = row['fields']['Post Title']
            match_row['assignee'] = row['fields']['Editor']['name']
            try:
                match_row['draft'] = row['fields']['Draft']
            except KeyError:  # no blog draft link
                match_row['draft'] = ""
                print('Blog with id #{} has no Draft link.'.format(row['id']))
            try:
                match_row['issue'] = row['fields']['Issue']
            except KeyError:  # No GitHub issue link
                print('Blog with id #{} has no Issue link.'.format(row['id']))
                match_row['issue'] = ""
            matches.append(match_row)
        return matches

    # def add_match_field(self, table_row, match_row):
    #     try:
    #         match_row['issue'] = table_row['fields']['Issue']
    #     except KeyError:  # No GitHub issue link
    #         print('Blog with id #{} has no Issue link.'.format(table_row['id']))
    #         match_row['issue'] = ""

    @property
    def filtered_table(self):
        return self._filtered_table
