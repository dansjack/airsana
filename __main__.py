from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
from util.date import *
from util.file import *


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


p = get_profile('Dan test', 'credentials.json')
latest = get_latest_datetime()
airtable = Airtable(p['airtable']['base'], p['airtable']['table'],
                    api_key=p['airtable']['api'])


table_fetcher = TableFetcher(airtable, p['airtable']['name'],
                             latest)
task_master_dan = Taskmaster(p['asana']['pat'], p['asana']['workspace_name'])
# task_master_jane = Taskmaster(jane_asana_pat, jane_asana_workspace_name)

set_latest_datetime(table_fetcher)
main_loop(table_fetcher, task_master_dan)
# main_loop(table_fetcher, task_master_jane)
