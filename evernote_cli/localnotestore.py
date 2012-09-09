import logging
import cPickle
import marshal
import types
from copy import copy
from functools import wraps

from evernote.edam.notestore.ttypes import NoteFilter

from evernoteconfig import Config

class LocalNoteStore(object):
    def __init__(self, note_store, changed_function):
        self.note_store = note_store
        self.changed_function = changed_function
        self.changed = changed_function()

        config = Config()
        operations_dir = config.get('caching', 'cache_directory')
        self.operations_file_name = operations_dir + '/local_note_store'
        with open(self.operations_file_name, 'r+') as operations_file:
            try:
                operations = cPickle.load(operations_file)
                self.operations = self._unmarshal_operations(operations)
            except EOFError:
                self.operations = {}

    def __getattr__(self, attr):
        logging.info('Calling %s', attr)
        return getattr(self.note_store, attr)

    def _changed(self, operation_key):
        self.changed = self.changed_function()
        if self.changed == self.operations[operation_key]['changed']:
            return False
        self.operations[operation_key]['changed'] = self.changed
        self._update_operations()
        return True

    def _get_operation_key(self, data_function, *args, **kwargs):
        #TODO: Find a nicer way to generate the key
        if data_function.__name__ == 'findNotesMetadata':
            return hash((data_function.__name__, args[1].notebookGuid))
        elif data_function.__name__ == 'getNote':
            return hash((data_function.__name__, args[1]))
        return hash(data_function.__name__)

    def _marshal_operations(self, operations):
        marshalled_operations = {}
        for operation_key, operation in operations.items():
            marshalled_operation = copy(operation)
            data_function = operation['data_function']
            marshalled_operation['data_function'] = marshal.dumps(data_function.func_code)
            marshalled_operations[operation_key] = marshalled_operation

        return marshalled_operations

    def _unmarshal_operations(self, operations):
        for operation_key, operation in operations.items():
            function_code = marshal.loads(operation['data_function'])
            operation['data_function'] = types.FunctionType(function_code,
                                                            globals())
            operations[operation_key] = operation

        return operations

    def _update_operations(self):
        with open(self.operations_file_name, 'w') as operations_file:
            operations = self._marshal_operations(self.operations)
            cPickle.dump(operations, operations_file)

    def _add_operation(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        logging.info('Calling %s', data_function.__name__)
        operation = {'data' : data_function(*args, **kwargs),
                     'data_function' : data_function,
                     'changed' : self.changed}
        self.operations[operation_key] = operation
        self._update_operations()

    def get_if_changed(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        if operation_key not in self.operations:
            self._add_operation(data_function, *args, **kwargs)
            return self.operations[operation_key]['data']

        if self._changed(operation_key):
            logging.info('Calling %s', data_function.__name__)
            new_data = data_function(*args, **kwargs)
            self.operations[operation_key]['data'] = new_data
            return new_data

        return self.operations[operation_key]['data']

    def listNotebooks(self, *args, **kwargs):
        data_function = self.note_store.listNotebooks
        return self.get_if_changed(data_function, *args, **kwargs)

    def findNotesMetadata(self, *args, **kwargs):
        data_function = self.note_store.findNotesMetadata
        return self.get_if_changed(data_function, *args, **kwargs)
    
    def getNote(self, *args, **kwargs):
        data_function = self.note_store.getNote
        return self.get_if_changed(data_function, *args, **kwargs)
