import markdown

from evernote.edam.type import ttypes

class Notebook(object):
    def __init__(self, edam_notebook):
        self.edam_notebook = edam_notebook
        self.name = edam_notebook.name
        self.guid = edam_notebook.guid

class Note(object):
    def __init__(self, edam_note=None, note_title=None):
        self.edam_note = edam_note
        if edam_note:
            #TODO: parse the html into markdown
            self.title = edam_note.title
            self.content = edam_note.content
        else:
            self.title = note_title
            self.content = None

    def get_edam_note(self):
        if self.edam_note:
            edam_note = self.edam_note
        else:
            edam_note = ttypes.Note()

        if self.content:
            html = markdown.markdown(self.content)
            edam_note.content = self._surround_with_html(html)
        edam_note.title = self.title

        return edam_note

    def _surround_with_html(self, text):
        return '<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{0}</en-note>'.format(text)

