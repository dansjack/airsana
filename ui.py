from airtable import Airtable

from airtable_fetcher import TableFetcher
from asana_taskmaster import Taskmaster
from util.date import get_latest_datetime, set_latest_datetime
from util.profile import get_profile, make_profile


def intro():
    print(
        """
        **************************************
        ********** Airtable to Asana *********
        **************************************
        
        Enter 'q' to quit at any time
        """)
    execute = False
    prof_name = ''
    while True:
        run_existing = input('Run script with existing profile (y/n): ').lower()
        if run_existing[0] == 'y':
            execute = True
            prof_name = input('profile name: ')
            break
        elif run_existing[0] == 'n':
            create_new = input('Create new profile (y/n): ').lower()
            if create_new[0] == 'y':
                print('Answer the following 9 questions to create a new '
                      'profile')
                make_profile()
        elif run_existing[0] == 'q':
            break
        else:
            print("Did not understand command. Please enter 'y', 'n', or 'q'")

    if execute:
        profile = get_profile(prof_name)

        airtable = Airtable(profile['airtable']['base'],
                            profile['airtable']['table'],
                            api_key=profile['airtable']['api'])

        table_fetcher = TableFetcher(airtable, profile['airtable']['name'],
                                     get_latest_datetime())

        task_master = Taskmaster(profile['asana']['pat'],
                                     profile['asana']['workspace_name'])
        set_latest_datetime(table_fetcher)
        return table_fetcher, task_master
