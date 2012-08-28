import ConfigParser
import logging
from os.path import dirname

from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from evernote.edam.userstore import UserStore

config = ConfigParser.RawConfigParser()
print dirname(__file__)
config.read(dirname(__file__) + '/evernotecli.cfg')
developer_token = config.get('login_details', 'developer_token')

def get_note_store_url():
    user_store_url = 'http://sandbox.evernote.com/edam/user'
    user_store_client = THttpClient(user_store_url)
    user_store_protocol = TBinaryProtocol(user_store_client)
    user_store = UserStore.Client(user_store_protocol,
                                  user_store_protocol)

    note_store_url = user_store.getNoteStoreUrl(developer_token)
    logging.debug('Retrieved NoteStore url: %s', note_store_url)

    return note_store_url
