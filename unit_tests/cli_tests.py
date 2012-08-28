from nose.tools import istest, assert_equal
from mock import patch

from testapi import TestApi
from evernotecli import EvernoteCli

notes = {'book1' : [{'name' : 'note1', 'uuid' : 1},
                    {'name' : 'note2', 'uuid' : 2}],
         'book2' : [{'name' : 'note1', 'uuid' : 3},
                    {'name' : 'note3', 'uuid' : 4}]}

@istest
def notebook_notes_are_listed_correctly():
    cli = setup_cli()

    default_notes = cli.list_notes()
    assert_equal(notes['book1'], default_notes)

    book2_notes = cli.list_notes('book2')
    assert_equal(notes['book2'], book2_notes)

@istest
def notebooks_are_listed_correctly():
    cli = setup_cli()

    notebooks = cli.list_notebooks()
    assert_equal(notebooks, ['book1', 'book2'])

@istest
@patch.object(EvernoteCli, 'edit_file', return_value=None)
@patch.object(TestApi, 'update_note')
@patch.object(TestApi, 'create_note')
def new_notes_are_created(create_note_method, update_note_method, edit_file_method):
    cli = setup_cli()
    cli.edit_or_add('new_note', 'book1')
    assert_equal(0, update_note_method.call_count)
    assert_equal(1, create_note_method.call_count)

def setup_cli():
    default_notebook = 'book1'

    api = TestApi(notes)
    cli = EvernoteCli(default_notebook, api)
    
    return cli
