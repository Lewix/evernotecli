from nose.tools import istest, assert_equal
from mock import patch

from testapi import TestApi
from evernotecli import EvernoteCli

notes = {'book1' : [{'title' : 'note1', 'uuid' : 1},
                    {'title' : 'note2', 'uuid' : 2}],
         'book2' : [{'title' : 'note1', 'uuid' : 3},
                    {'title' : 'note3', 'uuid' : 4}]}

@istest
def notebook_notes_are_listed_correctly():
    cli = setup_cli()

    default_notes = cli.list_notes()
    expected_titles = [note['title'] for note in notes['book1']]
    actual_titles = [note.title for note in default_notes]
    assert_equal(expected_titles, actual_titles)

    book2_notes = cli.list_notes('book2')
    expected_titles = [note['title'] for note in notes['book2']]
    actual_titles = [note.title for note in book2_notes]
    assert_equal(expected_titles, actual_titles)

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

    cli.edit_or_add('note1', 'book1')
    assert_equal(1, update_note_method.call_count)
    assert_equal(1, create_note_method.call_count)

def setup_cli():
    default_notebook = 'book1'

    api = TestApi(notes)
    cli = EvernoteCli(default_notebook, api)
    
    return cli
