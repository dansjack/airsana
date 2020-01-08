from datetime import datetime, timedelta
import json
import re


def get_latest_datetime(profile_name, file):
    """
    Find when the latest airtable row was created
    :param profile_name: name of the profile to search
    :param file: path of the file containing the profile
    :return: String. The most recent airtable row's datetime
    """
    created_time = ''
    with open(file, 'r') as f:
        print('GETTING latest createdTime...')
        data = json.load(f)
        for prof in data:
            if prof['name'] == profile_name:
                created_time = prof['airtable']['latest_createdTime']
                break
        date_compile = re.compile(r"^20[0-2]\d-((0\d)|1[1-2])-"
                                  r"((0\d)|([1-2][0-9])|30|31)$")
        if created_time is '':
            return '{}T00:00:00.000Z'\
                .format(datetime.now().date() - timedelta(days=1))
        elif date_compile.match(created_time):
            return '{}T00:00:00.000Z'\
                .format(created_time)

        else:
            return created_time


def set_latest_datetime(matcher, profile_name, file, days_ago=None):
    """
    Find when the latest airtable row was created
    :param matcher: TableMatcher object
    :param profile_name: name of the profile to update
    :param file: path of the file containing the profile
    :param days_ago: optional. Set the latest_datetime to today minus x days
    :return: void. Sets the datetime of the latest match inside the named
    profile
    """
    last_checked = get_latest_datetime(profile_name, file)
    print('SETTING latest createdTime...')
    for match in matcher.all_matches:
        if match['createdTime'] > last_checked:
            last_checked = match['createdTime']

    with open(file) as f:
        data = json.load(f)
        for prof in data:
            if prof['name'] == profile_name:
                prof['airtable']['latest_createdTime'] = last_checked

    with open(file, 'w', encoding='utf-8') as f:
        if days_ago is not None:
            json.dump('{}T00:00:00.000Z'.format(
                datetime.now().date() - timedelta(days=days_ago)))
        else:
            json.dump(data, f, ensure_ascii=False, indent=4)
