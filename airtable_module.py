from airtable import Airtable



airtable = Airtable('appxihFX0qEmouKsg', 'Content production',
                    api_key='keyHPaW1yiQPDcJFN').get_all()


def filter_by_assigned(table, name):
    """
    :param table: Instance of Airtable.get_all()
    :param name: Assigned name to filter by
    :return: List of Airtable rows assigned to :param name
    """
    filtered_table = list()
    for row in table:
        if row['fields']['Author']['name'] == name:
            filtered_table.append(row)
    return filtered_table


filtered_table = filter_by_assigned(airtable, 'Cameron Toth')
for i in filtered_table:
    print(i)
    print("\n")



# 1. Pull data from airtable calendar when: blog is assigned to Janey (editor
# column),
# 2. place data in an object
# 3. Send and add object to Asana
