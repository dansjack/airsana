from datetime import datetime, timedelta
import json


def get_latest_datetime(profile_name, days_ago=None):
    ca = ''
    with open('credentials.json', 'r') as f:
        print('GETTING latest createdTime...')
        data = json.load(f)
        for prof in data:
            if prof['name'] == profile_name:
                ca = prof['airtable']['latest_createdTime']
                break

        if ca is '':
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=1))
        elif days_ago is not None:
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=days_ago))
        else:
            return ca


def set_latest_datetime(fetcher, profile_name):
    last_checked = get_latest_datetime(profile_name)
    print('SETTING latest createdTime...')
    for match in fetcher.filtered_table:
        if match['createdTime'] > last_checked:
            last_checked = match['createdTime']

    with open('credentials.json') as f:
        data = json.load(f)
        for prof in data:
            if prof['name'] == profile_name:
                prof['airtable']['latest_createdTime'] = last_checked

    with open('credentials.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
