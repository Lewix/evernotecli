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

    def _changed(self):
        changed_value = self.changed_function()
        if changed_value == self.changed:
            return False
        self.changed = changed_value
        return True

    def _get_operation_key(self, data_function, *args, **kwargs):
        #TODO: Find a nicer way to generate the key
        if len(args) > 1 and isinstance(args[1], NoteFilter):
            return hash((data_function.__name__, args[1].notebookGuid))
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

    def _add_operation(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        logging.info('Calling %s', data_function.__name__)
        operation = {'data' : data_function(*args, **kwargs),
                     'data_function' : data_function}
        self.operations[operation_key] = operation
        with open(self.operations_file_name, 'w') as operations_file:
            operations = self._marshal_operations(self.operations)
            cPickle.dump(operations, operations_file)

    def get_if_changed(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        if operation_key not in self.operations:
            self._add_operation(data_function, *args, **kwargs)
            return self.operations[operation_key]['data']

        if self._changed():
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
