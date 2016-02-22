from skytap.models.Note import Note
from skytap.models.SkytapGroup import SkytapGroup
from skytap.framework.ApiClient import ApiClient
import json


class Notes(SkytapGroup):
    def __init__(self, note_json, env_url):
        super(Notes, self).__init__()
        self.load_list_from_json(note_json, Note)
        self.url = env_url + '/notes.json'

    def add(self, note):
        api = ApiClient()
        data = {"text": note}
        response = api.rest(self.url, data, 'POST')
        self.refresh()
        return response

    def delete(self, note):
        api = ApiClient()
        url = self.url.replace('.json', '/' + str(note.id))
        response = api.rest(url,
                            {},
                            'DELETE')
        self.refresh()
        return response

    def delete_all(self):
        keys = self.data.keys()
        for key in keys:
            self.delete(self.data[key])

    def refresh(self):
        if len(self.url) == 0:
            return KeyError
        api = ApiClient()
        note_json = api.rest(self.url)
        self.load_list_from_json(note_json, Note)