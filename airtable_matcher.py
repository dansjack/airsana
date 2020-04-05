class TableMatcher:
    def __init__(self, airtable, profile, last_fetched):
        """
        Takes an Airtable object and filters the rows by a filter value and
        by createdTime. It then creates a list of dicts to send to Asana
        :param airtable: Airtable object. from the Airtable API
        :param profile: dict. a profile containing the user's credentials and
        other data necessary to transfer the data
        :param last_fetched: string. the created time of the row fetched the
        last time the program was ran (or what the user set it to in
        profiles.json, manually)
        """
        self._profile = profile
        self._match_structure = self._profile['airtable'][
            'match_structure']
        self._last_fetched = last_fetched
        self._airtable = airtable
        self._all_matches = self._get_matches()

    def _get_matches(self):
        """
        Filters Airtable.get_all() by self._profile's filter and filter
        value
        :return: List<Dict>. List of dict matches
        """
        print('GETTING matches with createdTime later than {}'.format(
            self._last_fetched))
        view = ''
        if self._profile['airtable']['view']:
            view = self._profile['airtable']['view']

        return [row for row in self._airtable.search(
            self._profile['airtable']['filter'],
            self._profile['airtable']['filter_value'],
            view=view) if row['createdTime'] > self._last_fetched]

    def prep_matches(self):
        """
        List of matches ready to get pushed to an Asana workspace
        :return: List<Dict>. List of matches
        """
        if self._all_matches:
            return [self.prep_match_helper(row) for row in self._all_matches]
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
    def all_matches(self):
        """
        :return: List<Dict> All raw matches from an Airtable object
        """
        return self._all_matches
