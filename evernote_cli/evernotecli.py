#!/usr/bin/python2.7
"""note.

Usage:
    note ls [<notebook>]
    note notebooks
    note print [<title>] [--notebook=<notebook_name>]
    note [<title>] [--notebook=<notebook_name>]
"""

import os
import string
import sys
import select
import tempfile
import cProfile
import logging
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

    def _get_notebook_name(self, notebook_name):
        if not notebook_name:
            return self.default_notebook
        else:
            return notebook_name

    def _get_note_content(self, note):
        return HTML2Text().handle(unicode(note.content, 'utf_8'))


    def list_notes(self, notebook_name=None):
        notebook_name = self._get_notebook_name(notebook_name)
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

        notes.reverse()
        for note in notes:
            print note.title

    def print_note(self, note_title, notebook_name):
        notebook_name = self._get_notebook_name(notebook_name)
        note = self.api.get_note(note_title, notebook_name)

        if note is None:
            print 'Note {1} does not exist'.format(note_title)
            return

        print self._get_note_content(note)

    def edit_or_add(self, note_title, notebook_name):
        #TODO: do something to deal with duplicate notes
        notebook_name = self._get_notebook_name(notebook_name)

        temp_file = tempfile.NamedTemporaryFile(delete=False)
        note = self.api.get_note(note_title, notebook_name)

        if note is not None:
            markdown_content = self._get_note_content(note)
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

if __name__ == '__main__':
    arguments = docopt(__doc__)

    titles = []
    if select.select([sys.stdin],[],[],0.0)[0]:
        titles = [title[:-1] for title in sys.stdin.readlines()]
    if arguments['<title>']:
        titles.append(arguments['<title>'])

    logging.basicConfig(filename='/tmp/evernotelog', level=logging.DEBUG)
    logging.info('Running %s', string.join(sys.argv))
    config = Config()
    default_notebook = config.get('defaults', 'default_notebook')

    cli = EvernoteCli(default_notebook)

    if arguments['ls']:
        cli.print_notes(arguments['<notebook>'])
    elif arguments['notebooks']:
        cli.print_notebooks()
    elif arguments['print']:
        for title in titles:
            print 'Printing note {0}'.format(title)
            cli.print_note(title, arguments['--notebook'])
    elif len(titles) > 0:
        for title in titles:
            print 'Editing note {0}'.format(title)
            cli.edit_or_add(title, arguments['--notebook'])
