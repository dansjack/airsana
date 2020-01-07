# /usr/bin/python3
from pathlib import Path
from ui import user_select_profile
from airtable import Airtable
from airtable_matcher import TableMatcher
from asana_taskmaster import Taskmaster
from util.date import *


def main_loop(taskmaster, table_rows, nf_list):
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            notes = main_loop_helper(nf_list, row)
            taskmaster.add_task(row['title'], notes)
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


def main_loop_helper(note_fields, table_row):
    notes = ''
    for note_field in note_fields:
        notes += '{}: {}\n\n'.format(note_field.capitalize(),
                                     table_row[note_field])
    return notes


def initialize_objects(profile, file):
    """

    :param profile: profile to pull data from/send to
    :param file: file path of the profile
    :return: TableMatcher instance, Taskmaster instance
    """
    if profile['name'] == 'TEST PROFILE':  # ensures proper imports in terminal
        file = (Path(__file__).parent / "./profile_example.json").resolve()
    airtable = Airtable(profile['airtable']['base'],
                        profile['airtable']['table'],
                        api_key=profile['airtable']['api'])
    matcher = TableMatcher(airtable, profile,
                           get_latest_datetime(profile['name'], file))

    taskmaster = Taskmaster(profile)
    set_latest_datetime(matcher, profile['name'], file)
    return matcher, taskmaster


if __name__ == '__main__':
    file = (Path(__file__).parent / "./profiles.json").resolve()
    profile = user_select_profile(file)
    if profile is not None:
        nf_list = profile['asana']['note_fields']
        m, t = initialize_objects(profile, file)
        prepped_matches = m.prep_matches()
        if m is not None:
            main_loop(t, prepped_matches, nf_list)

    print("""
        *****************************
        ********** Goodbye **********
        *****************************
        """)
