import random

from nose.tools import istest, assert_is_not_none, assert_in

from evernoteapi import EvernoteApi
from notes import Note

#TODO: is_not_none doesn't test much...
def authentication_is_successful():
    api = EvernoteApi()
    note_store_url = api._get_note_store_url()
    assert_is_not_none(note_store_url)

def note_store_is_retrieved_successfully():
    api = EvernoteApi()
    note_store = api._get_note_store()
    assert_is_not_none(note_store)

def notebooks_are_listed_successfully():
    api = EvernoteApi()
    notebooks = api.list_notebooks()
    assert_is_not_none(notebooks)

def notes_are_listed_successfully():
    api = EvernoteApi()
    notes = api.list_notes("lewix's notebook")
    assert_is_not_none(notes)

@istest
def notes_are_created_successfully():
    api = EvernoteApi()
    note_title = str(random.random())
    note = Note(note_title=note_title)
    note.content = 'test note'

    api.create_note(note, "lewix's notebook")
    
    notes = api.list_notes("lewix's notebook")
    note_titles = [note.title for note in notes]
    assert_in(note_title, note_titles)
