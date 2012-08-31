from nose.tools import istest, assert_in, assert_not_in, assert_equal

from changesstore import ChangesStore
from localnotestore import LocalNoteStore, cache
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


@istest
def local_store_only_updates_when_there_are_changes():
    note_store = LocalNoteStore()
    changed_function = Mock(return_value=1)
    data_function = Mock()

    note_store.get_if_changed(changed_function, data_function)
    note_store.get_if_changed(changed_function, data_function)

    assert_equal(data_function.call_count, 1)
    changed_function.return_value = 2

    note_store.get_if_changed(changed_function, data_function)
    note_store.get_if_changed(changed_function, data_function)

    assert_equal(data_function.call_count, 2)


@istest
def cache_decorator_caches_output_until_changes():
    note_store = LocalNoteStore()
    changed_function = Mock(return_value=1)
    call_counter = Mock()

    @cache(changed_function, note_store)
    def data_function(arg):
        call_counter()

    data_function(1)
    data_function(1)
    assert_equal(call_counter.call_count, 1)

    changed_function.return_value = 2
    data_function(1)
    data_function(1)
    assert_equal(call_counter.call_count, 2)
