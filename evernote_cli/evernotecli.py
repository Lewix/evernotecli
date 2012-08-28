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
        pass

    def print_notebooks(self):
        for notebook in self.list_notebooks():
            print notebook

    def print_notes(self, notebook_name):
        for note in self.list_notes(notebook_name):
            print note

    def edit_or_add(self, note_title, notebook_name):
        pass

if __name__ == '__main__':
    arguments = docopt(__doc__)

    config = ConfigParser.RawConfigParser()
    config.read(dirname(__file__) + '/evernotecli.cfg')
    default_notebook = config.get('defaults', 'default_notebook')

    print arguments

    cli = EvernoteCli(default_notebook)


    if arguments['notebooks']:
        cli.print_notebooks()
    elif arguments['ls']:
        cli.print_notes(arguments['<notebook>'])
    elif arguments['<title>']:
        cli.edit_or_add(arguments['<title>'], arguments['<notebook>'])
