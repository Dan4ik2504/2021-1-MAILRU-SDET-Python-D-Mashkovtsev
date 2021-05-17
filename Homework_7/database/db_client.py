import copy

import exceptions


class DBTable:

    def __init__(self, *columns):
        self._db = []
        self._columns = ('entry_id', *columns)
        self._last_id = 1

    def validate_columns(self, columns_list):
        if not all([k in self._columns for k in columns_list]):
            raise exceptions.KeyDoesntExists(f'One of given columns does not exists. Columns: {columns_list}')

    def select(self, **kwargs):
        self.validate_columns(kwargs.keys())

        resp = copy.deepcopy(self._db)
        for k, v in kwargs.items():
            resp = filter(lambda entry: entry.get(k) == v, resp)

        return list(resp)

    def insert(self, **kwargs):
        self.validate_columns(kwargs.keys())
        if 'entry_id' in kwargs:
            if kwargs['entry_id'] <= self._last_id:
                if len(self.select(id=kwargs['entry_id'])) > 0:
                    raise exceptions.EntryExists(f'Entry with id "{kwargs["entry_id"]}" already exists')
        else:
            kwargs['entry_id'] = self._last_id
        self._db.append(copy.deepcopy(kwargs))
        self._last_id += 1
        return kwargs

    def update(self, entry_id, **kwargs):
        self.validate_columns(kwargs.keys())
        for entry in self._db:
            if entry['entry_id'] == entry_id:
                for k, v in kwargs.items():
                    entry[k] = v

    def delete(self, entry_id):
        self._db = [e for e in self._db if e['entry_id'] != entry_id]

    def truncate(self):
        self._db = []
        self._last_id = 1

    def exists(self, **kwargs):
        return len(self.select(**kwargs)) > 0