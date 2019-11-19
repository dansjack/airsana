from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
from credentials import *


def main_loop(fetcher, taskmaster):
    table_rows = fetcher.prep_matches()
    if len(table_rows) == 0:
        print('No new tasks to add to Asana. Asana is up to date.')
    else:
        for row in table_rows:
            taskmaster.add_task(row['title'], 'Draft: {}\n\nIssue: {}'
                                .format(row['draft'], row['issue']))


def get_latest_datetime():
    with open('created_at.txt', 'r') as date_time:
        print('GETTING last createdTime...')
        return date_time.read()


def set_latest_datetime(fetcher):
    latest = fetcher.get_latest_match_time()
    print('SETTING latest createdTime...')
    with open('created_at.txt', 'w') as date_time:
        date_time.write(latest)


airtable = Airtable(jane_at_base,
                    jane_at_table,
                    api_key=jane_at_api)


table_fetcher = TableFetcher(airtable,
                             jane_at_name,
                             get_latest_datetime())
task_master_dan = Taskmaster(dan_asana_pat, 'NSC')
# task_master_jane = Taskmaster(jane_asana_pat, jane_asana_workspace_name)

set_latest_datetime(table_fetcher)
main_loop(table_fetcher, task_master_dan)
