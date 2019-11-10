import asana


class Taskmaster:
    def __init__(self, pat, workspace_name):
        """
        Connects to an Asana user's workspace and adds tasks to it

        :param pat: Asana Personal Access Token
        :param workspace_name: The workspace name to add a task to
        """

        self._pat = pat
        self._client = asana.Client().access_token(self._pat)
        self._set_client_options()
        self._workspace_name = workspace_name
        self._workspace_gid = self._get_workspace_gid()
        self._assignee = self._client.users.me()

    def _set_client_options(self):
        """
        Sets client options, suppresses Asana deprecation warnings

        :return void
        """
        self._client.LOG_ASANA_CHANGE_WARNINGS = False
        self._client.options['pretty'] = True
        self._client.options['item_limit'] = 50
        self._client.options['fields'] = ["this.name", "this.assignee.name",
                                          "this.notes", "this.due_on",
                                          "this.completed"]

    def _get_workspace_gid(self):
        for workspace in self._client.workspaces.find_all():
            if workspace['name'] == self._workspace_name:
                return workspace['gid']
        return -1

    def find_all_incomplete(self):
        for task in self._client.tasks.find_all(workspace=self._workspace_gid,
                                                assignee=self._assignee['gid']):
            if not task['completed']:
                print(task)

    def add_task(self, name, notes):
        """
        Posts a task to the object's workspace

        :param name: Name of the task
        :param notes: Notes for the task
        :return: void
        """
        self._client.tasks.create_in_workspace(self._workspace_gid,
                                               {'name': name,
                                                'notes': notes,
                                                'assignee': self._assignee})

        print('Task named "{}" added to workspace: {}'
              .format(name, self._workspace_name))
