import evernotecli
from nose.tools import istest, assert_is_not_none

@istest
def test_authentication_is_successful():
    note_store_url = evernotecli._get_note_store_url()
    assert_is_not_none(note_store_url)

@istest
def test_note_store_is_retrieved_successfully():
    note_store = evernotecli.get_note_store()
    assert_is_not_none(note_store)
