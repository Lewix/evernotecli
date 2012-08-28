from nose.tools import istest, assert_is_not_none

from evernoteapi import EvernoteApi

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
