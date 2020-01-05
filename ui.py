from airtable import Airtable

from airtable_matcher import TableMatcher
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
              'profile\n3. Run script with test profile')
        run_existing = input(
            'Enter a command by digit: ').lower()
        if run_existing[0] == '1':  # Run with existing profile
            print('Enter the name of one of the profiles listed')
            names = get_profile_names('credentials.json')
            print_profile_names(names)
            profile_name = input('profile name: ')
            if profile_name not in names:
                print('That profile name does not exist. Returning to '
                      'previous menu...')
            else:
                return get_profile(profile_name, 'credentials.json')

        elif run_existing[0] == '2':  # Make new profile
            print('Answer the following 14 questions to create a new profile')
            make_profile('credentials.json')
            print('New profile created')
        elif run_existing[0] == '3':  # Run with example profile
            print('Running script with test profile...')
            return get_profile('TEST PROFILE', 'cred_example.json')
        elif run_existing[0] == 'q':
            break
        else:
            print("Did not understand command. Please enter 'y', 'n', "
                  "or 'q'...")


def initialize_objects(profile):
    airtable = Airtable(profile['airtable']['base'],
                        profile['airtable']['table'],
                        api_key=profile['airtable']['api'])
    fetcher = TableMatcher(airtable, profile['airtable']['filter_value'],
                           get_latest_datetime(profile['name'],
                                               'credentials.json'), profile[
                               'airtable']['match_structure'])

    fetcher.get_matches(profile['airtable']['filter'])

    taskmaster = Taskmaster(profile['asana']['pat'],
                            profile['asana']['workspace_name'])
    set_latest_datetime(fetcher, profile['name'])
    return fetcher, taskmaster

