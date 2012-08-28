from nose.tools import istest, assert_equal

from testapi import TestApi
from evernotecli import EvernoteCli

@istest
def notebook_notes_are_listed_correctly():
    notes = {'book1' : ['note1',
                         'note2'],
             'book2' : ['note1',
                        'note3']}
    default_notebook = 'book1'
    
    api = TestApi(notes)
    cli = EvernoteCli(default_notebook, api)

    default_notes = cli.list_notes()
    assert_equal(notes['book1'], default_notes)

    book2_notes = cli.list_notes('book2')
    assert_equal(notes['book2'], all_notes)
