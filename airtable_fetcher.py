def add_match_field(table_row, structure_vals):
    """
    Catch any missing data in one row of an Airtable calendar
    :param table_row: dict<String:String>. an airtable calendar row
    :param fields: list<String>. A list of fields
    :return:
    """
    match_row = dict()
    for fields in structure_vals:
        field = fields[0]
        sub_field = None
        if len(fields) == 2:
            sub_field = fields[1]

        f_lower = field.lower()
        if sub_field == 'name':
            f_lower = 'assignee'
        elif 'title' in field.lower() or 'headline' in field.lower():
            f_lower = 'title'

        if sub_field:
            try:
                match_row[f_lower] = table_row['fields'][field][sub_field]
            except KeyError:  # No value at field/sub-field for this match
                print('Blog with id #{} has no value at: ["{}"]["{}"]...'.format(
                    table_row['id'], field, sub_field))
                match_row[f_lower] = ""
        else:
            try:
                match_row[f_lower] = table_row['fields'][field]
            except KeyError:  # No value at field for this match
                print('Blog with id #{} has no value at: ["{}"]...'.format(
                    table_row['id'], field))
                match_row[f_lower] = ""
    return match_row


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
        print('GETTING matches with createdTime later than {}'.format(
            self._last_fetched))
        local_filtered = []
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

    def print_matches(self, match_structure, asana_preview=False):
        """
        For testing purposes only
        :param match_structure:
        :param asana_preview:
        :return:
        """
        table = self._filtered_table
        if asana_preview:
            table = self.prep_matches(match_structure)
        for i in table:
            print(i)
            print("\n")

    def prep_matches(self, match_structure):
        if not self._filtered_table:
            return -1
        return [add_match_field(row, match_structure.values()) for row in
                self._filtered_table]

    @property
    def filtered_table(self):
        return self._filtered_table
