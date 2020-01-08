import asana


class Taskmaster:
    def __init__(self, profile):
        """
        Connects to an Asana user's workspace and adds tasks to it. Stores
        :param profile: dict. User profile object
        """
        self._profile = profile
        self._pat = self._profile['asana']['pat']
        self._workspace_name = self._profile['asana']['workspace_name']
        self._client = asana.Client().access_token(self._pat)
        self._set_client_options()
        self._workspace_gid = self._get_workspace_gid()
        self._assignee = self._client.users.me()

    def _set_client_options(self):
        """
        Sets client options, suppresses Asana deprecation warnings
        :return void.
        """
        self._client.LOG_ASANA_CHANGE_WARNINGS = False
        self._client.options['pretty'] = True
        self._client.options['item_limit'] = 50
        self._client.options['fields'] = ["this.name", "this.assignee.name",
                                          "this.notes", "this.due_on",
                                          "this.completed"]

    def _get_workspace_gid(self):
        """
        Returns the Asana workspace id given self._workspace_name
        :return: string. Asana workspace ID
        """
        for workspace in self._client.workspaces.find_all():
            if workspace['name'] == self._workspace_name:
                return workspace['gid']
        return '-1'

    def _find_all_incomplete(self):
        """
        For testing purposes only. Prints all tasks marked 'incomplete' in asana
        :return: void.
        """
        for task in self._client.tasks.find_all(workspace=self._workspace_gid,
                                                assignee=self._assignee['gid']):
            if not task['completed']:
                print(task)

    def add_task(self, name, notes):
        """
        Posts a task to the workspace at self._workspace_gid. Tasks are assigned
        to the user at :param name and the task description contains the
        information stored in :param notes
        :param name: Name of the task
        :param notes: Notes for the task
        :return: void.
        """
        # TODO: Add "due on" dates. Pull from Airtable
        self._client.tasks.create_in_workspace(self._workspace_gid,
                                               {'name': name,
                                                'notes': notes,
                                                'assignee': self._assignee})
