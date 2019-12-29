from airtable import Airtable
from airtable_fetcher import TableFetcher
from ui import intro, initialize_objects
from util.date import get_latest_datetime, set_latest_datetime
from util.profile import get_profile


def main_loop(fetcher, taskmaster, table_rows):
    # table_rows = fetcher.prep_matches()
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            notes = 'Draft: {}\n\nIssue: {}'.format(row['draft'], row['issue'])
            taskmaster.add_task(row['title'], notes)
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


profile, is_execute = intro()
f, t = initialize_objects(profile, is_execute)
if f is not None:
    main_loop(f, t, f.prep_matches(profile['airtable']['match_structure']))
print("""
    *****************************
    ********** Goodbye **********
    *****************************
    """)


# dan_test = get_profile('Dan test')
# airtable = Airtable(dan_test['airtable']['base'],
#                     dan_test['airtable']['table'],
#                     api_key=dan_test['airtable']['api'])
# table_fetcher = TableFetcher(airtable, dan_test['airtable']['name'],
#                              get_latest_datetime())
#
# print(table_fetcher.print_matches())

# dan_test2 = get_profile('Dan test2')
# print(dan_test2)
# airtable2 = Airtable(dan_test2['airtable']['base'],
#                     dan_test2['airtable']['table'],
#                     api_key=dan_test2['airtable']['api'])
#
# table_fetcher2 = TableFetcher(airtable2, dan_test2['airtable']['name'],
#                               get_latest_datetime(dan_test2['name']))
# print(table_fetcher2.print_matches())
# set_latest_datetime(table_fetcher2, dan_test2['name'])
# task_master_jane = Taskmaster(jane_test['asana']['pat'],
#                              jane_test['asana']['workspace_name'])
# main_loop(table_fetcher, task_master_jane)
