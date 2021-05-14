import copy

import exceptions


class DBTable:
    _last_id = 0

    def __init__(self, *columns):
        self._db = []
        self._columns = ('id', *columns)

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
        self._last_id += 1
        if 'id' in kwargs:
            if kwargs['id'] <= self._last_id:
                if len(self.select(id=kwargs['id'])) > 0:
                    raise exceptions.EntryExists(f'Entry with id "{kwargs["id"]}" already exists')
        else:
            kwargs['id'] = self._last_id
        self._db.append(copy.deepcopy(kwargs))
        return kwargs
