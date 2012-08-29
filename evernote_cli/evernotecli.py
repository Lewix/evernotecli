#!/usr/bin/python2.7
"""note.

Usage:
    note ls [<notebook>]
    note notebooks
    note <title> [<notebook>]
"""

import os
import tempfile
from os.path import dirname, realpath

from docopt import docopt

from evernoteapi import EvernoteApi
from evernoteconfig import Config
from notes import Note

class EvernoteCli(object):
    def __init__(self, default_notebook, api=None):
        if api:
            self.api = api
        else:
            self.api = EvernoteApi()

        self.default_notebook = default_notebook

    def list_notes(self, notebook_name=None):
        if not notebook_name:
            notes = self.api.list_notes(self.default_notebook)
        else:
            notes = self.api.list_notes(notebook_name)

        return notes

    def list_notebooks(self):
        return self.api.list_notebooks()

    def print_notebooks(self):
        notebooks = self.list_notebooks()
        if not notebooks:
            return

        for notebook in notebooks:
            print notebook.name

    def print_notes(self, notebook_name):
        notes = self.list_notes(notebook_name)
        if not notes:
            return

        for note in notes:
            print note.title

    def edit_or_add(self, note_title, notebook_name):
        creating = True
        with tempfile.NamedTemporaryFile() as temp_file:
            for note_object in self.list_notes(notebook_name):
                if note_object.title == note_title:
                    creating = False
                    note = note_object
                    temp_file.write(note.content)
                    break
            else:
                note = Note(note_title=note_title)
                self.edit_file(temp_file.name) 
                note.content = temp_file.read()

            if creating:
                self.api.create_note(note, notebook_name)
            else:
                self.api.update_note(note)

    def edit_file(self, file_name):
        os.system('vim {0}'.format(file_name))

if __name__ == '__main__':
    arguments = docopt(__doc__)

    config = Config()
    default_notebook = config.get('defaults', 'default_notebook')

    cli = EvernoteCli(default_notebook)


    if arguments['notebooks']:
        cli.print_notebooks()
    elif arguments['ls']:
        cli.print_notes(arguments['<notebook>'])
    elif arguments['<title>']:
        cli.edit_or_add(arguments['<title>'], arguments['<notebook>'])
