from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
from util.date import *
from util.profile import *


def main_loop(fetcher, taskmaster):
    table_rows = fetcher.prep_matches()
    if table_rows == -1:
        print('No new tasks to add to Asana')
    else:
        for row in table_rows:
            taskmaster.add_task(row['title'], 'Draft: {}\n\nIssue: {}'
                                .format(row['draft'], row['issue']))
            print('Task named "{}" added to workspace'.format(row['title']))
    print('Done')


dan_test = get_profile('Dan test')

airtable = Airtable(dan_test['airtable']['base'], dan_test['airtable']['table'],
                    api_key=dan_test['airtable']['api'])
table_fetcher = TableFetcher(airtable, dan_test['airtable']['name'],
                             get_latest_datetime())
task_master_dan = Taskmaster(dan_test['asana']['pat'],
                             dan_test['asana']['workspace_name'])

# jane_test = get_profile('Jane test')
# task_master_jane = Taskmaster(jane_test['asana']['pat'],
#                              jane_test['asana']['workspace_name'])

set_latest_datetime(table_fetcher)
main_loop(table_fetcher, task_master_dan)
# main_loop(table_fetcher, task_master_jane)
