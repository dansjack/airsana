class TableMatcher:
    def __init__(self, airtable, profile, last_fetched):
        """
        Takes an Airtable object and filters the rows by a filter value and
        by createdTime. It then creates a list of dicts to send to Asana
        :param airtable: Airtable object. from airtable API
        :param profile: dict. a profile containing the user's credentials and
        other data necessary to transfer the data
        :param last_fetched: string. the created time of the row fetched the
        last time the program was ran (or what the user set it to in
        profiles.json, manually)
        """
        self._profile = profile
        self._match_structure = self._profile['airtable'][
            'match_structure'].values()
        self._last_fetched = last_fetched
        self._airtable = airtable
        self._filtered_table = self._get_matches()

    def _get_matches(self):
        """Filters Airtable.get_all() by assignee passed to Class """
        print('GETTING matches with createdTime later than {}'.format(
            self._last_fetched))
        return [row for row in self._airtable.search(
            self._profile['airtable']['filter'],
            self._profile['airtable']['filter_value']) if
            row['createdTime'] > self._last_fetched]

    def prep_matches(self):
        if self._filtered_table:
            return [self.prep_match_helper(row) for row in self._filtered_table]
        return -1

    def prep_match_helper(self, table_row):
        """
        Catch any missing data in one row of an Airtable calendar
        :param table_row: dict<String:String>. an airtable calendar row
        :return: dict<String:String>. Match ready to push to Asana
        """
        match_row = dict()  # TODO: Get profile object inside matcher
        for field in self._match_structure:
            f_lower = field.lower()
            if 'title' in field.lower() or 'headline' in field.lower():
                f_lower = 'title'
            try:
                match_row[f_lower] = table_row['fields'][field]
            except KeyError:  # No value at field for this match
                print('Blog with id #{} has no value at: ["{}"]...'.format(
                    table_row['id'], field))
                match_row[f_lower] = ""
        return match_row

    @property
    def filtered_table(self):
        return self._filtered_table
