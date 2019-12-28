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
    return profile


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
    profile['airtable']['name'] = input('Airtable profile owner name: ')
    profile['airtable']['api'] = input('Airtable API key: ')
    profile['airtable']['base'] = input('Airtable Base: ')
    profile['airtable']['table'] = input('Airtable table name: ')

    with open('credentials.json') as f:
        data = json.load(f)
        data.append(profile)
    with open('credentials.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def has_profile():
    with open('credentials.json') as f:
        if len(json.load(f)) == 0:
            return False
    return True
