from airtable import Airtable
from airtable_fetcher import TableFetcher
from ui import intro, initialize_objects
from util.date import get_latest_datetime, set_latest_datetime
from util.profile import get_profile


def main_loop(taskmaster, table_rows, nf_list):
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            notes = ''
            for note_field in nf_list:
                notes += '{}: {}\n\n'.format(
                    note_field.capitalize(), row[note_field])
            taskmaster.add_task(row['title'], notes)
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


profile, is_execute = intro()
struct = profile['airtable']['match_structure']
nf_list = profile['asana']['note_fields']
f, t = initialize_objects(profile, is_execute)
prepped_matches = f.prep_matches(struct)

if f is not None:
    main_loop(t, prepped_matches, nf_list)
print("""
    *****************************
    ********** Goodbye **********
    *****************************
    """)