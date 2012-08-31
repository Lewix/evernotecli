#!/usr/bin/python2.7
"""note.

Usage:
    note ls [<notebook>]
    note notebooks
    note refresh
    note <title> [<notebook>]
"""

import os
import tempfile
from os.path import dirname, realpath

from docopt import docopt
from html2text import HTML2Text

from evernoteapi import EvernoteApi
from evernoteconfig import Config

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
        #TODO: do something to deal with duplicate notes
        if not notebook_name:
            notebook_name = self.default_notebook

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        note = self.api.get_note(note_title, notebook_name)

        if note is not None:
            markdown_content = HTML2Text().handle(note.content)
            temp_file.write(markdown_content)
            temp_file = self.edit_file(temp_file)
            content = temp_file.read()
            self.api.update_note(note_title, content, notebook_name)
        else:
            temp_file = self.edit_file(temp_file) 
            content = temp_file.read()
            self.api.create_note(note_title, content, notebook_name)

        temp_file.close()

    def edit_file(self, file_object):
        file_object.close()
        os.system('vim {0}'.format(file_object.name))
        return open(file_object.name, 'r')

    def refresh(self):
        self.api.retry_failed_operations()
        self.api.refresh_cache()

if __name__ == '__main__':
    arguments = docopt(__doc__)

    config = Config()
    default_notebook = config.get('defaults', 'default_notebook')

    cli = EvernoteCli(default_notebook)


    if arguments['ls']:
        cli.print_notes(arguments['<notebook>'])
    elif arguments['notebooks']:
        cli.print_notebooks()
    elif arguments['refresh']:
        cli.refresh()
    elif arguments['<title>']:
        cli.edit_or_add(arguments['<title>'], arguments['<notebook>'])
