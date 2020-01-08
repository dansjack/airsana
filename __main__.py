# /usr/bin/python3
from pathlib import Path
from ui import main_loop
from airtable import Airtable
from airtable_matcher import TableMatcher
from asana_taskmaster import Taskmaster
from util.date import *


def assign_rows(taskmaster, table_rows, note_fields):
    """
    Assigns rows in :param table_rows to the Asana workspace known by :param
    taskmaster
    :param taskmaster: Taskmaster object
    :param table_rows: All matches filtered through TableMatcher.prepMatches()
    :param note_fields: Note fields from profile the user wants included in
    the match sent to the Asana API
    :return: void.
    """
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            notes = assign_rows_helper(note_fields, row)
            taskmaster.add_task(row['title'], notes)
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


def assign_rows_helper(note_fields, table_row):
    """
    Builds and returns a String of notes from the fields specified in :param
    note_fields and populated with the data for those fields in :param
    table_row

    :param note_fields: Note fields from profile the user wants included in
    the match sent to the Asana API
    :param table_row:
    :return: String. A formatted string containing the notes listed in :param
    note_fields.
    """
    notes = ''
    for note_field in note_fields:
        notes += '{}: {}\n\n'.format(note_field.capitalize(),
                                     table_row[note_field])
    return notes


def initialize_objects(profile, file):
    """
    Instatiates objects needed for the program with profile data
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
    print("""  
        **************************************
        *************   Airsana   ************
        **************************************

        Enter 'q' to quit at any time
        """)
    file = (Path(__file__).parent / "./my-profiles.json").resolve()
    profile = main_loop(file)
    if profile is not None:
        nf_list = profile['asana']['note_fields']
        m, t = initialize_objects(profile, file)
        prepped_matches = m.prep_matches()
        if m is not None:
            assign_rows(t, prepped_matches, nf_list)

    print("""
        *****************************
        ********** Goodbye **********
        *****************************
        """)
