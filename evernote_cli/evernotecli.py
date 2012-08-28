#!/usr/bin/python2.7
"""note.

Usage:
    note <title> [<notebook>]
    note ls [<notebook>]
    note ls all
    note default [<notebook>]
"""

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
