class Notebook(object):
    def __init__(self, edam_notebook_object):
        self.edam_notebook_object = edam_notebook_object
        self.name = edam_notebook_object.name
        self.guid = edam_notebook_object.guid

class Note(object):
    def __init__(self, edam_note_object=None):
        self.edam_note_object = edam_note_object
        self.title = edam_note_object.title
