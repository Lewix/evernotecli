from uuid import uuid4
from notes import Note

class TestApi(object):
    def __init__(self, all_notes):
        self.notes = all_notes

    def list_notebooks(self):
        return self.notes.keys()

    def list_notes(self, notebook):
        notes = [Note(note_title=note['title'])
                 for note in self.notes[notebook]]
        for note in notes:
            note.content = ''

        return notes

    def create_note(self, note, notebook_name):
        pass

    def update_note(self, note, notebook_name):
        pass
