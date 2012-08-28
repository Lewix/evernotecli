import evernotecli
from nose.tools import istest, assert_is_not_none

@istest
def test_authentication_is_successful():
    note_store_url = evernotecli.get_note_store_url()
    assert_is_not_none(note_store_url)
