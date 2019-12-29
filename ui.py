from airtable import Airtable

from airtable_fetcher import TableFetcher
from asana_taskmaster import Taskmaster
from util.date import get_latest_datetime, set_latest_datetime
from util.profile import get_profile, make_profile


def intro():
    print("""
        **************************************
        ********** Airtable to Asana *********
        **************************************
        
        Enter 'q' to quit at any time
        """)
    execute = False
    prof_name = ''
    cont = True
    while cont:
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
                print('New profile created')
            elif create_new[0] == 'n':
                print('returning to previous question...')
                continue
            elif create_new[0] == 'q':
                break
            else:
                print(
                    "Did not understand command. Please enter 'y', 'n', or 'q'")
        elif run_existing[0] == 'q':
            break
        else:
            print("Did not understand command. Please enter 'y', 'n', or 'q'")
    profile = get_profile(prof_name)

    return profile, execute


def initialize_objects(profile, execute):
    if execute:
        airtable = Airtable(profile['airtable']['base'],
                            profile['airtable']['table'],
                            api_key=profile['airtable']['api'])
        fetcher = TableFetcher(airtable, profile['airtable']['filter_value'],
                               get_latest_datetime(profile['name']))

        if len(profile['airtable']['filter']) == 2:  # sub filter exists
            fetcher.get_matches(profile['airtable']['filter'][0],
                                profile['airtable']['filter'][1])
        else:  # no sub filter
            fetcher.get_matches(profile['airtable']['filter'][0])

        taskmaster = Taskmaster(profile['asana']['pat'],
                                profile['asana']['workspace_name'])
        set_latest_datetime(fetcher, profile['name'])
        return fetcher, taskmaster
    else:
        return None, None
