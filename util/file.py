import json


def get_profile(name, file):
    profile = {}
    with open(file) as f:
        data = json.load(f)
        for prof in data:
            if prof['name'] == name:
                profile['name'] = prof['name']
                profile['asana'] = prof['asana']
                profile['airtable'] = prof['airtable']
                break
    return profile
