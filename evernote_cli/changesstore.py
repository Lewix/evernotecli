#TODO: persist these operations, otherwise this is pointless
class ChangesStore(object):
    def __init__(self):
        self.saved_operations = []

    def try_or_save(self, function, developer_token, note):
        try:
            function(developer_token, note)
        except:
            operation = (function, developer_token, note)
            self.saved_operations.append(operation)

    def retry_failed_operations(self):
        for operation in self.saved_operations:
            self.saved_operations.remove(operation)
            self.try_or_save(*operation)
