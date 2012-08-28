from nose.tools import istest, assert_is_not_none

from evernoteapi import EvernoteApi

@istest
def test_authentication_is_successful():
    api = EvernoteApi()
    note_store_url = api._get_note_store_url()
    assert_is_not_none(note_store_url)

@istest
def test_note_store_is_retrieved_successfully():
    api = EvernoteApi()
    note_store = api.get_note_store()
    assert_is_not_none(note_store)
