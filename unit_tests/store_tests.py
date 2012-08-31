from nose.tools import istest, assert_in, assert_not_in

from changesstore import ChangesStore
from mock import Mock

def create_excepting_note_store():
    note_store = Mock()
    note_store.updateNote.side_effect = Exception()
    return note_store

note_store = create_excepting_note_store()
developer_token = Mock()
note = 'note with modified content'
operation = (note_store.updateNote, developer_token, note)


@istest
def notes_are_saved_when_note_store_throws():
    changes_store = ChangesStore()
    changes_store.try_or_save(note_store.updateNote, developer_token, note)

    assert_in(operation, changes_store.saved_operations)


@istest
def operations_are_retried_on_refresh():
    changes_store = ChangesStore()
    changes_store.try_or_save(note_store.updateNote, developer_token, note)
    note_store.updateNote.side_effect = None
    changes_store.retry_failed_operations()

    assert_not_in(operation, changes_store.saved_operations)
