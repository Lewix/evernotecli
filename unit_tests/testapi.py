from uuid import uuid4

from evernote.edam.type import ttypes

class TestApi(object):
    def __init__(self, all_notes):
        self.notes = all_notes

    def list_notebooks(self):
        return self.notes.keys()

    def list_notes(self, notebook_name):
        notes = []
        for note in self.notes[notebook_name]:
            edam_note = ttypes.Note()
            edam_note.content = ''
            edam_note.title = note['title']
            notes.append(edam_note)

        return notes

    def create_note(self, note_title, content, notebook_name):
        pass

    def update_note(self, note_title, content, notebook_name):
        pass

    def get_note(self, note_title, notebook_name):
        for note in self.list_notes(notebook_name):
            if note.title == note_title:
                return note
