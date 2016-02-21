from skytap.framework.ApiClient import ApiClient
import json


class SkytapResource(object):
    def __init__(self, initial_json):
        self.data = {}
        for k, v in initial_json.iteritems():
            self.data[k] = v
        self._calculate_custom_data()

    def refresh(self):
        if 'url' not in self.data:
            return KeyError
        api = ApiClient()
        env_json = api.rest(self.url)
        self.__init__(json.loads(env_json))

    def _calculate_custom_data(self):
        pass

    def __getattr__(self, key):
        """Make the values accessible.

        This allows all user values to be available via calls like:
        user.id
        """
        if key not in self.data:
            raise AttributeError
        return self.data[key]

    def details(self):
        det = ''
        for x in self.data:
            det += str(x) + ": " + str(self.data[x]) + '\n'
        return det

    def json(self):
        return json.dumps(self.data, indent=4)

    def __str__(self):
        return '[' + self.id + '] ' + self.name

    def __int__(self):
        return int(self.id)

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __contains__(self, key):
        return key in self.data