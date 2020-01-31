from pathlib import Path
from util.profile import *


def main_loop(file):
    """
    :param file: path of file containing a list of profiles
    :return: dict. The profile selected by the user
    """
    while True:
        print('Commands:\n1. Run script with existing profile\n2. Make new '
              'profile\n3. Run script with test profile')
        run_existing = input(
            'Enter a command by digit: ').lower()
        if run_existing[0] == '1':  # Run with existing profile
            names = get_profile_names(file)
            if not names:
                print('No profiles found. Add a profile to profiles.json '
                      'and re-start the program.')
                break
            else:
                print('Enter the name of one of the profiles listed')
                print_profile_names(names)
                profile_name = input('profile name: ')
                if profile_name not in names:
                    print('That profile name does not exist. Returning to '
                          'previous menu...')
                else:
                    return get_profile(profile_name, file)

        elif run_existing[0] == '2':  # Make new profile
            print('Answer the following 14 questions to create a new profile')
            make_profile(file)
            print('New profile created')
        elif run_existing[0] == '3':  # Run with example profile
            print('Running script with test profile...')
            return get_profile('TEST PROFILE', (Path(__file__).parent /
                               "./profile_example.json").resolve())
        elif run_existing[0] == 'q':
            break
        else:
            print("Did not understand command. Please enter 'y', 'n', "
                  "or 'q'...")
