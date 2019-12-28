from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
from ui import intro
from util.date import *
from util.profile import *


def main_loop(fetcher, taskmaster):
    table_rows = fetcher.prep_matches()
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            taskmaster.add_task(row['title'],
                                'Draft: {}\n\nIssue: {}'.format(row['draft'],
                                                                row['issue']))
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


f, t = intro()
main_loop(f, t)


# jane_test = get_profile('Jane test')

# airtable = Airtable(jane_test['airtable']['base'],
#                     jane_test['airtable']['table'],
#                     api_key=jane_test['airtable']['api'])
# table_fetcher = TableFetcher(airtable, jane_test['airtable']['name'],
#                              get_latest_datetime())
# task_master_jane = Taskmaster(jane_test['asana']['pat'],
#                              jane_test['asana']['workspace_name'])
# main_loop(table_fetcher, task_master_jane)
