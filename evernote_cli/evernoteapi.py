import logging
from os.path import dirname, realpath

import markdown
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.type import ttypes
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
from evernote.edam.limits.constants import EDAM_USER_NOTES_MAX

from evernoteconfig import Config
from changesstore import ChangesStore
from localnotestore import LocalNoteStore, cache

#TODO: better error handling
#TODO: fix this shit with a nested class called CachedOperations?

local_note_store = LocalNoteStore()
config = Config()


def _get_store_protocol(store_url):
    user_store_client = THttpClient(store_url)
    return TBinaryProtocol(user_store_client)

def _get_note_store_url():
    user_store_url = config.get('login_details', 'user_store_url')
    user_store_protocol = _get_store_protocol(user_store_url)
    user_store = UserStore.Client(user_store_protocol,
                                  user_store_protocol)

    developer_token = config.get('login_details', 'developer_token')
    note_store_url = user_store.getNoteStoreUrl(developer_token)
    logging.debug('Retrieved NoteStore url: %s', note_store_url)

    return note_store_url

def _get_note_store():
    note_store_url = _get_note_store_url()
    note_store_protocol = _get_store_protocol(note_store_url)

    note_store = NoteStore.Client(note_store_protocol,
                                  note_store_protocol)
    logging.debug('Retrived NoteStore: %s', note_store)

    return note_store

note_store = _get_note_store()


def changed_function():
    developer_token = config.get('login_details', 'developer_token')
    sync_state = note_store.getSyncState(developer_token)
    return sync_state.updateCount


class EvernoteApi(object):
    def __init__(self):
        self._developer_token = config.get('login_details', 'developer_token')
        self.note_store = _get_note_store()
        self.changes_store = ChangesStore()


    @cache(changed_function, local_note_store)
    def list_notebooks(self):
        notebooks = self.note_store.listNotebooks(self._developer_token)
        return notebooks

    def get_notebook_guid(self, notebook_name):
        for notebook in self.list_notebooks():
            if notebook.name.lower() == notebook_name.lower():
                return notebook.guid
        else:
            print 'Notebook {0} not found'.format(notebook_name)
            exit()

    def _list_subset_of_notes(self, notebook_name, start, end):
        notebook_guid = self.get_notebook_guid(notebook_name)
        note_filter = NoteFilter(notebookGuid=notebook_guid,
                                 ascending=False,
                                 order=1)
        result_spec = NotesMetadataResultSpec(includeTitle=True)
        note_list = self.note_store.findNotesMetadata(self._developer_token,
                                                      note_filter,
                                                      start,
                                                      end,
                                                      result_spec)
        return (note_list.notes, note_list.totalNotes)

    @cache(changed_function, local_note_store)
    def list_notes(self, notebook_name):
        #TODO: no longer need to split this up in a loop
        all_notes = []
        increment = 1000 # Getting more than 50 doesn't seem to work
        start = 0

        (notes, total_notes) = self._list_subset_of_notes(notebook_name,
                                                          start,
                                                          start+increment)
        all_notes.extend(notes)
        while total_notes > start+increment:
            start += increment
            (notes, total_notes) = self._list_subset_of_notes(notebook_name,
                                                              start,
                                                              start+increment)
            all_notes.extend(notes)

        return [note for note in all_notes]

    def create_note(self, note_title, note_content, notebook_name):
        note = ttypes.Note()
        note.title = note_title
        note.notebookGuid = self.get_notebook_guid(notebook_name)
        note.content = self._create_note_content(note_content)

        def create_and_invalidate_notes_cache(developer_token, note):
            cache.invalidate(self.list_notes, notebook_name)
            self.note_store.createNote(self._developer_token, note)

        self.changes_store.try_or_save(create_and_invalidate_notes_cache,
                                       self._developer_token,
                                       note)

    def get_note(self, note_title, notebook_name):
        for note in self.list_notes(notebook_name):
            if note.title.lower() == note_title.lower():
                return self.note_store.getNote(self._developer_token,
                                               note.guid,
                                               True, False,
                                               False, False)

    def update_note(self, note_title, note_content, notebook_name):
        note = self.get_note(note_title, notebook_name)
        old_content = note.content
        note.content = self._create_note_content(note_content)
        if old_content != note.content:
            self.changes_store.try_or_save(self.note_store.updateNote,
                                           self._developer_token,
                                           note)

    def retry_failed_operations(self):
        self.changes_store.retry_failed_operations()

    def refresh_cache(self):
        cache.invalidate(self._get_note_store_url)
        self.note_store = self._get_note_store()
        cache.invalidate(self.list_notebooks)
        for notebook in self.list_notebooks():
            cache.invalidate(self.list_notes, notebook.name)
            self.list_notes(notebook.name)

    def _create_note_content(self, note_content):
        html_content = markdown.markdown(note_content)
        return self._surround_with_html(html_content)

    def _surround_with_html(self, text):
        return '<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{0}</en-note>'.format(text)
