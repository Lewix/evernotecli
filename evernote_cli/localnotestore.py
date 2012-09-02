from functools import wraps

#TODO: Persist stuff

class LocalNoteStore(object):
    def __init__(self, note_store, changed_function):
        self.operations = {}
        self.note_store = note_store
        self.changed_function = changed_function
        self.changed = changed_function()

    def __getattr__(self, attr):
        return getattr(self.note_store, attr)

    def _changed(self):
        changed_value = self.changed_function()
        if changed_value == self.changed:
            return False
        self.changed = changed_value
        return True

    def _get_operation_key(self, data_function, *args, **kwargs):
        return hash((data_function, args, frozenset(kwargs.items())))

    def _add_operation(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        operation = {'data' : data_function(*args, **kwargs),
                     'data_function' : data_function}
        self.operations[operation_key] = operation

    def get_if_changed(self, data_function, *args, **kwargs):
        operation_key = self._get_operation_key(data_function, *args, **kwargs)
        if operation_key not in self.operations:
            self._add_operation(data_function, *args, **kwargs)
            return self.operations[operation_key]['data']

        if self._changed():
            new_data = data_function(*args, **kwargs)
            self.operations[operation_key]['data'] = new_data
            return new_data

        return self.operations[operation_key]['data']

    def listNotebooks(self, *args, **kwargs):
        #TODO: not actually getting called. Need to put the adapter on Client
        data_function = self.note_store.listNotebooks
        return self.get_if_changed(data_function, *args, **kwargs)

    def findNotesMetadata(self, *args, **kwargs):
        data_function = self.note_store.listNotebooks
        return self.get_if_changed(data_function, *args, **kwargs)
    
    def getNote(self, *args, **kwargs):
        data_function = self.note_store.getNote
        return self.get_if_changed(data_function, *args, **kwargs)
