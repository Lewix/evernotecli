#!/usr/bin/python2.7
"""note.

Usage:
    note <title> [<notebook>]
    note ls [<notebook>]
    note notebooks
"""

from docopt import docopt

from evernoteapi import EvernoteApi

class EvernoteCli(object):
    def __init__(self, default_notebook, api=None):
        if api:
            self.api = api
        else:
            self.api = EvernoteApi()

        self.default_notebook = default_notebook

    def list_notes(self, notebook=None):
        if not notebook:
            notes = self.api.list_notes(self.default_notebook)
        else:
            notes = self.api.list_notes(notebook)

        return notes

    def print_notebooks(self):
        pass

    def print_notes(notebook_name):
        pass

    def edit_or_add(note_title, notebook_name):
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
        cli.edit_or_add(arguments['<title>'], arguments['<notebook>')
