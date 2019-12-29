from airtable import Airtable

from airtable_fetcher import TableFetcher
from asana_taskmaster import Taskmaster
from util.date import *
from util.profile import *


def user_select_profile():
    print("""
        **************************************
        ********** Airtable to Asana *********
        **************************************
        
        Enter 'q' to quit at any time
        """)
    while True:
        print('Commands:\n1. Run script with existing profile\n2. Make new '
              'profile')
        run_existing = input(
            'Enter a command by digit: ').lower()
        if run_existing[0] == '1':  # Run with existing profile
            print('Enter the name of one of the profiles listed')
            names = get_profile_names()
            print_profile_names(names)
            profile_name = input('profile name: ')
            if profile_name not in names:
                print('That profile name does not exist. Returning to '
                      'previous menu...')
            else:
                return get_profile(profile_name)

        elif run_existing[0] == '2':  # Make new profile
            print('Answer the following 11 questions to create a new profile')
            make_profile()
            print('New profile created')
        elif run_existing[0] == 'q':
            break
        else:
            print("Did not understand command. Please enter 'y', 'n', "
                  "or 'q'...")


def initialize_objects(profile):
    print(profile)
    airtable = Airtable(profile['airtable']['base'],
                        profile['airtable']['table'],
                        api_key=profile['airtable']['api'])
    fetcher = TableFetcher(airtable, profile['airtable']['filter_value'],
                           get_latest_datetime(profile['name']), profile[
                               'airtable']['match_structure'])

    fetcher.get_matches(profile['airtable']['filter'])

    taskmaster = Taskmaster(profile['asana']['pat'],
                            profile['asana']['workspace_name'])
    set_latest_datetime(fetcher, profile['name'])
    return fetcher, taskmaster

