

class TableFetcher:
    def __init__(self, airtable, assignee, last_fetched, match_structure):
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
        self._match_structure = match_structure.values()

    def get_matches(self, fields):
        """Filters Airtable.get_all() by assignee passed to Class """
        print('GETTING matches with createdTime later than {}'.format(
            self._last_fetched))
        field_name = fields[0]
        sub_field = None
        if len(fields) == 2:
            sub_field = fields[1]

        local_filtered = [row for row in self._airtable.get_all() if row[
            'createdTime'] > self._last_fetched]

        self._filtered_table = [row for row in local_filtered if
                                self.get_matches_helper(row, field_name,
                                                        sub_field)]

    def get_matches_helper(self, table_row, field_name, sub_field):
        try:
            if sub_field and table_row['fields'][field_name][
                sub_field] == self._assignee or table_row['fields'][field_name]\
                    == self._assignee:
                return True
        except KeyError:  # blog not assigned
            print('Blog with id #{} not assigned. Skipping...'.format(
                table_row['id']))
            return False

    def prep_matches(self):
        if self._filtered_table:
            return [self.prep_match_helper(row) for row in self._filtered_table]
        return -1

    def prep_match_helper(self, table_row):
        """
        Catch any missing data in one row of an Airtable calendar
        :param table_row: dict<String:String>. an airtable calendar row
        :return: dict<String:String>. Match object ready to push to Asana
        """
        match_row = dict()
        for fields in self._match_structure:
            field = fields[0]
            sub_field = None
            if len(fields) == 2:
                sub_field = fields[1]

            f_lower = field.lower()
            if sub_field == 'name':
                f_lower = 'assignee'
            elif 'title' in field.lower() or 'headline' in field.lower():
                f_lower = 'title'
            try:
                if sub_field:
                    match_row[f_lower] = table_row['fields'][field][sub_field]
                else:
                    match_row[f_lower] = table_row['fields'][field]
            except KeyError:  # No value at field for this match
                if sub_field:
                    print('Blog with id #{} has no value at: ["{}"]["{}"]...'.
                          format(table_row['id'], field, sub_field))
                else:
                    print('Blog with id #{} has no value at: ["{}"]...'.
                          format(table_row['id'], field))
                match_row[f_lower] = ""
        return match_row

    @property
    def filtered_table(self):
        return self._filtered_table
