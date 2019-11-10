from airtable import Airtable
from asana_taskmaster import Taskmaster
from airtable_fetcher import TableFetcher
import credentials


airtable = Airtable(credentials.jane_at_base, credentials.jane_at_table,
                    api_key=credentials.jane_at_api)

table_fetcher = TableFetcher(airtable,
                             credentials.jane_at_name,
                             '2019-11-01T19:07:39.000Z')
table_fetcher.print_matches(asana_preview=True)
task_master = Taskmaster(credentials.dan_asana_pat, 'NSC')


def main_loop(fetcher, taskmaster):
    table_rows = fetcher.prep_matches()
    for row in table_rows:
        taskmaster.add_task(row['title'], 'Draft: {}\n\nIssue: {}'.format(
            row['draft'], row['issue']))


# print(table_fetcher.get_latest_match_time())
main_loop(table_fetcher, task_master)


