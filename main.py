from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
import credentials


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
        print('GETTING...')
        return date_time.read()


def set_latest_datetime(fetcher):
    latest = fetcher.get_latest_match_time()
    print('SETTING...')
    with open('created_at.txt', 'w') as date_time:
        date_time.write(latest)


airtable = Airtable(credentials.jane_at_base,
                    credentials.jane_at_table,
                    api_key=credentials.jane_at_api)


table_fetcher = TableFetcher(airtable,
                             credentials.jane_at_name,
                             get_latest_datetime())
task_master = Taskmaster(credentials.dan_asana_pat, 'NSC')

set_latest_datetime(table_fetcher)

main_loop(table_fetcher, task_master)
