from datetime import datetime, timedelta


def get_latest_datetime():
    with open('created_at.txt', 'r') as date_time:
        print('GETTING latest createdTime...')
        if len(date_time.read()) == 0:
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=1))
        else:
            date_time.seek(0)
            return date_time.read()


def set_latest_datetime(fetcher):
    last_checked = get_latest_datetime()
    print('SETTING latest createdTime...')
    for match in fetcher.filtered_table:
        if match['createdTime'] > last_checked:
            last_checked = match['createdTime']
    with open('created_at.txt', 'w') as date_time:
        date_time.write(last_checked)
