import random

from nose.tools import istest, assert_is_not_none, assert_in
from mock import patch

import evernotecli
from evernoteapi import EvernoteApi

#TODO: is_not_none doesn't test much...
#TODO: always use sandbox

@istest
def authentication_is_successful():
    api = EvernoteApi()
    note_store_url = api._get_note_store_url()
    assert_is_not_none(note_store_url)

@istest
def note_store_is_retrieved_successfully():
    api = EvernoteApi()
    note_store = api._get_note_store()
    assert_is_not_none(note_store)

@istest
def notebooks_are_listed_successfully():
    api = EvernoteApi()
    notebooks = api.list_notebooks()
    assert_is_not_none(notebooks)

@istest
def notes_are_listed_successfully():
    api = EvernoteApi()
    notes = api.list_notes("lewix's notebook")
    assert_is_not_none(notes)

@istest
def notes_are_created_successfully():
    api = EvernoteApi()

    note_title = str(random.random())
    content = 'test note'
    api.create_note(note_title, content, "notebook2")
    
    notes = api.list_notes("notebook2")
    note_titles = [note.title for note in notes]
    assert_in(note_title, note_titles)
