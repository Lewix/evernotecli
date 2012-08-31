from functools import wraps

#TODO: store different operations for same function with different args
class LocalNoteStore(object):
    def __init__(self):
        self.operations = {}

    def _add_operation(self, changed_function, data_function, *args, **kwargs):
        operation = {'changed' : changed_function(),
                     'changed_function' : changed_function,
                     'data' : data_function(*args, **kwargs),
                     'data_function' : data_function}
        self.operations[data_function] = operation

    def get_if_changed(self, changed_function, data_function, *args, **kwargs):
        if data_function not in self.operations:
            self._add_operation(changed_function,
                                data_function, *args, **kwargs)
            return self.operations[data_function]['data']

        changed = self.operations[data_function]['changed']
        new_changed = self.operations[data_function]['changed_function']()
        if changed != new_changed:
            self.operations[data_function]['changed'] = new_changed
            return data_function(*args, **kwargs)

        return self.operations[data_function]['data']

def cache(changed_function, local_note_store):
    def cache_decorator(data_function):
        @wraps(data_function)
        def wrapper(*args, **kwargs):
            return local_note_store.get_if_changed(changed_function,
                                                   data_function,
                                                   *args, **kwargs)

        return wrapper
    return cache_decorator
