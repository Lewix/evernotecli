from uuid import uuid4

from nose.tools import istest, assert_equal, assert_less_equal
from mock import patch, MagicMock

from evernote.edam.type.ttypes import Notebook
from evernote.edam.notestore.ttypes import NoteList

from evernoteapi import EvernoteApi

notebooks = [Notebook(name="lewix's notebook", defaultNotebook=True, serviceUpdated=1346097626000, sharedNotebookIds=None, sharedNotebooks=None, updateSequenceNum=1, published=None, serviceCreated=1346097626000, guid='85115409-5dad-4feb-90c9-64b187dde336', stack=None, publishing=None)]
notes = NoteList(notes=[])

@istest
def check_notebooks_are_looked_up_in_cache():
    api = make_mock_api()

    api.list_notebooks()
    api.list_notebooks()

    assert_less_equal(api.note_store.listNotebooks.call_count, 1)

@istest
def refresh_clears_the_cache():
    api = make_mock_api()

    api.refresh_cache()
    assert_equal(api.note_store.listNotebooks.call_count, 1)

    api.list_notebooks()
    assert_equal(api.note_store.listNotebooks.call_count, 1)

def make_mock_api():
    with patch.object(EvernoteApi, '_get_note_store'):
        api = EvernoteApi()
    api.note_store = MagicMock()
    api.note_store.listNotebooks = MagicMock(return_value=notebooks)
    api.note_store.findNotes = MagicMock(return_value=notes)
    api.note_store.getNote = MagicMock()
    return api
