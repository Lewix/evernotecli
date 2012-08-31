import logging
from functools import wraps

class LocalNoteStore(object):
    def __init__(self):
        self.operations = {}

    def _add_operation(self, changed_function, data_function):
        operation = {'changed' : changed_function(),
                     'changed_function' : changed_function,
                     'data' : data_function(),
                     'data_function' : data_function}
        self.operations[data_function] = operation

    def get_if_changed(self, changed_function, data_function):
        if data_function not in self.operations:
            self._add_operation(changed_function, data_function)
            return self.operations[data_function]['data']

        changed = self.operations[data_function]['changed']
        new_changed = self.operations[data_function]['changed_function']()
        if changed != new_changed:
            self.operations[data_function]['changed'] = new_changed
            return data_function()

        return self.operations[data_function]['data']

def cache(changed_function, local_note_store):
    def cache_decorator(data_function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            local_note_store.get_if_changed(changed_function,
                                            data_function)

        return wrapper
    return cache_decorator
