class TestApi(object):
    def __init__(self, notes):
        self.notes = notes

    def list_notebooks(self, notebook):
        return self.notes.keys()

    def list_notes(self, notebook):
        return self.notes[notebook]
