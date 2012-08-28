from uuid import uuid4

class TestApi(object):
    def __init__(self, all_notes):
        self.notes = all_notes

    def list_notebooks(self):
        return self.notes.keys()

    def list_notes(self, notebook):
        return self.notes[notebook]
