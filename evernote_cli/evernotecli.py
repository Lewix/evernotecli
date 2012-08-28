#!/usr/bin/python2.7
"""note.

Usage:
    note ls [<notebook>]
    note notebooks
    note <title> [<notebook>]
"""

import ConfigParser
from os.path import dirname

from docopt import docopt

from evernoteapi import EvernoteApi

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
            print note

    def edit_or_add(self, note_title, notebook_name):
        pass

    def edit_file(file_name):
        pass

if __name__ == '__main__':
    arguments = docopt(__doc__)

    config = ConfigParser.RawConfigParser()
    config.read(dirname(__file__) + '/evernotecli.cfg')
    default_notebook = config.get('defaults', 'default_notebook')

    cli = EvernoteCli(default_notebook)


    if arguments['notebooks']:
        cli.print_notebooks()
    elif arguments['ls']:
        cli.print_notes(arguments['<notebook>'])
    elif arguments['<title>']:
        cli.edit_or_add(arguments['<title>'], arguments['<notebook>'])
