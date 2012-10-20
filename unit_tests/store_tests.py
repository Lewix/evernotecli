from nose.tools import istest, assert_in, assert_not_in, assert_equal, assert_less_equal

from changesstore import ChangesStore
from localnotestore import LocalNoteStore
from mock import Mock, patch

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


@istest
@patch('cPickle.dump')
@patch('marshal.dumps')
def local_store_only_updates_when_there_are_changes(pickle_dump, marshal_dump):
    changed_function = Mock(return_value=1)
    note_store = get_note_store()
    local_note_store = LocalNoteStore(note_store, changed_function)
    data_function = Mock()
    data_function.__name__ = 'data_function'

    local_note_store.get_if_changed(data_function)
    local_note_store.get_if_changed(data_function)

    assert_equal(data_function.call_count, 1)
    changed_function.return_value = 2

    local_note_store.get_if_changed(data_function)
    local_note_store.get_if_changed(data_function)

    assert_equal(data_function.call_count, 2)


@istest
@patch('cPickle.dump')
@patch('marshal.dumps')
def local_store_keeps_separate_operations_for_different_arguments(pickle_dump, marshal_dump):
    changed_function = Mock(return_value=1)
    note_store = get_note_store()
    local_note_store = LocalNoteStore(note_store, changed_function)
    data_function = Mock()
    data_function.__name__ = 'data_function'

    local_note_store.get_if_changed(data_function, 1)
    local_note_store.get_if_changed(data_function, 2)

    assert_equal(data_function.call_count, 2)


@istest
@patch('cPickle.dump')
@patch('marshal.dumps')
def local_store_wraps_edam_note_store(pickle_dump, marshal_dump):
    note_store = get_note_store()
    changed_function = Mock(return_value=1)
    local_note_store = LocalNoteStore(note_store, changed_function)

    local_note_store.listNotebooks()
    local_note_store.listNotebooks()
    
    assert_equal(note_store.listNotebooks.call_count, 1)
    changed_function.return_value = 2

    local_note_store.listNotebooks()
    local_note_store.listNotebooks()

    assert_equal(note_store.listNotebooks.call_count, 2)


@istest
@patch('cPickle.dump')
def local_store_persists_data(pickle_dump):
    note_store = get_note_store()
    note_store.listNotebooks.__name__ = 'listNotebooks'
    def listNotebooks(*args, **kwargs):
        return []
    note_store.listNotebooks.func_code = listNotebooks.func_code

    local_note_store = LocalNoteStore(note_store, Mock())
    local_note_store.listNotebooks()
    local_note_store = LocalNoteStore(note_store, Mock())
    local_note_store.listNotebooks()

    assert_equal(note_store.listNotebooks.call_count, 1)

def get_note_store():
    note_store = Mock()
    note_store.listNotebooks.__name__ = 'listNotebooks'
    return note_store
