import json


def get_profile(name):
    """
    :param name: profile name
    :return: dict of selected profile
    """
    profile = {}
    with open('credentials.json') as f:
        data = json.load(f)
        for prof in data:
            if prof['name'] == name:
                profile['name'] = prof['name']
                profile['asana'] = prof['asana']
                profile['airtable'] = prof['airtable']
                break
    if not profile:
        return None
    return profile


def print_profile_names(profile_names):
    for name in profile_names:
        print('- {}'.format(name))


def get_profile_names():
    profile_names = []
    with open('credentials.json') as f:
        data = json.load(f)
        for prof in data:
            profile_names.append(prof['name'])
    return profile_names


def make_profile():
    """
    :return: void. Adds a new profile to credentials.json
    """
    profile = {'name': input('Profile name: '), 'asana': {}, 'airtable': {}}
    profile['asana']['name'] = input("Asana profile owner name: ")
    profile['asana']['pat'] = input('Asana PAT: ')
    profile['asana']['id'] = input('Asana ID: ')
    profile['asana']['workspace_id'] = input('Asana workspace ID: ')
    profile['asana']['workspace_name'] = input('Asana workspace name: ')
    profile['airtable']['filter_value'] = input('Airtable profile owner name: ')
    profile['airtable']['api'] = input('Airtable API key: ')
    profile['airtable']['base'] = input('Airtable Base: ')
    profile['airtable']['table'] = input('Airtable table name: ')
    profile['airtable']['latest_createdTime'] = ''  # TODO: get user input
    profile['airtable']['filter'] = ''  # TODO: get user input

    with open('credentials.json') as f:
        data = json.load(f)
        data.append(profile)
    with open('credentials.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
