import random

from nose.tools import istest, assert_is_not_none, assert_in, assert_equal
from mock import patch

import evernotecli
from evernoteapi import EvernoteApi
from sandboxconfig import SandboxConfig
from evernoteconfig import Config

#TODO: is_not_none doesn't test much...
#TODO: always use sandbox
#TODO: patch api to not use cache

@istest
def authentication_is_successful():
    api = get_api_and_refresh_cache()
    note_store_url = api._get_note_store_url()
    assert_is_not_none(note_store_url)

@istest
def note_store_is_retrieved_successfully():
    api = get_api_and_refresh_cache()
    note_store = api._get_note_store()
    assert_is_not_none(note_store)

@istest
def notebooks_are_listed_successfully():
    api = get_api_and_refresh_cache()
    notebooks = api.list_notebooks()
    assert_is_not_none(notebooks)

@istest
def notes_are_listed_successfully():
    api = get_api_and_refresh_cache()
    notes = api.list_notes("lewix's notebook")
    assert_is_not_none(notes)

@istest
def notes_are_created_successfully():
    api = get_api_and_refresh_cache()

    note_title = str(random.random())
    content = 'test note'
    api.create_note(note_title, content, "notebook2")
    
    notes = api.list_notes("notebook2")
    note_titles = [note.title for note in notes]
    assert_in(note_title, note_titles)

@istest
def notes_are_retrieved_successfully():
    api = get_api_and_refresh_cache()

    note_title = 'get_note test'
    notebook_name = "lewix's notebook"

    note = api.get_note(note_title, notebook_name)
    assert_is_not_none(note)
    assert_in('test', note.content)

@istest
def notes_are_updated_successfully():
    api = get_api_and_refresh_cache()

    note_title = 'update_note test'
    notebook_name = "lewix's notebook"
    content = str(random.random())
    api.update_note(note_title, content, notebook_name)

    updated_note = api.get_note(note_title, notebook_name)
    assert_in(content, updated_note.content)

def get_api_and_refresh_cache():
    api = EvernoteApi()
    assert_equal('True', api.config.get('testing', 'use_sandbox'))
    api.refresh_cache()
    return api
