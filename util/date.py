from datetime import datetime, timedelta
import json
import re


def get_latest_datetime(profile_name, days_ago=None):
    created_time = ''
    with open('credentials.json', 'r') as f:
        print('GETTING latest createdTime...')
        data = json.load(f)
        for prof in data:
            if prof['name'] == profile_name:
                created_time = prof['airtable']['latest_createdTime']
                break
        date_compile = re.compile(r"20[0-2]\d-((0\d)|1[1-2])-(0\d)|([1-2]["
                                  "0-9])|30|31")
        if created_time is '':
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=1))
        elif days_ago is not None:
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=days_ago))
        elif date_compile.match(created_time):
            return '{}T00:00:00.000Z'\
                .format(created_time)
        else:
            return created_time


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
