import logging
from os.path import dirname, realpath

import markdown

from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.type import ttypes
from evernote.edam.userstore import UserStore
from evernote.edam.notestore import NoteStore
from evernote.edam.notestore.ttypes import NoteFilter
from evernote.edam.limits.constants import EDAM_USER_NOTES_MAX

from evernoteconfig import Config

#TODO: better error handling
#TODO: reduce number of API calls
#TODO: cache stuff

class EvernoteApi(object):
    def __init__(self):
        self.config = Config()
        self._developer_token = self.config.get('login_details', 'developer_token')
        self.note_store = self._get_note_store()


    def _get_store_protocol(self, store_url):
        user_store_client = THttpClient(store_url)
        return TBinaryProtocol(user_store_client)

    def _get_note_store_url(self):
        user_store_url = self.config.get('login_details', 'user_store_url')
        user_store_protocol = self._get_store_protocol(user_store_url)
        user_store = UserStore.Client(user_store_protocol,
                                      user_store_protocol)

        note_store_url = user_store.getNoteStoreUrl(self._developer_token)
        logging.debug('Retrieved NoteStore url: %s', note_store_url)

        return note_store_url

    def _get_note_store(self):
        note_store_url = self._get_note_store_url()
        note_store_protocol = self._get_store_protocol(note_store_url)

        note_store = NoteStore.Client(note_store_protocol,
                                      note_store_protocol)
        logging.debug('Retrived NoteStore: %s', note_store)

        return note_store

    def list_notebooks(self):
        notebooks = self.note_store.listNotebooks(self._developer_token)
        return [notebook for notebook in notebooks]

    def get_notebook_guid(self, notebook_name):
        for notebook in self.list_notebooks():
            if notebook.name == notebook_name:
                return notebook.guid
        else:
            print 'Notebook {0} not found'.format(notebook_name)
            return None

    def list_notes(self, notebook_name):
        #TODO: pagination
        notebook_guid = self.get_notebook_guid(notebook_name)
        note_filter = NoteFilter(notebookGuid=notebook_guid,
                                 ascending=False,
                                 order=1)
        note_list = self.note_store.findNotes(self._developer_token,
                                              note_filter,
                                              0,
                                              EDAM_USER_NOTES_MAX)

        return [note for note in note_list.notes]

    def create_note(self, note_title, note_content, notebook_name):
        edam_note = ttypes.Note()
        edam_note.title = note_title
        html_content = markdown.markdown(note_content)
        edam_note.content = self._surround_with_html(html_content)
        new_note = self.note_store.createNote(self._developer_token, edam_note)

    def update_note(self, note_title, note_content, notebook_name):
        pass

    def _surround_with_html(self, text):
        return '<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note>{0}</en-note>'.format(text)
