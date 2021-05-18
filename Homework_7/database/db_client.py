import copy
import logging

import exceptions
import settings

logger = logging.getLogger(settings.DATABASE_SETTINGS.LOGGER_NAME)


def kwargs_to_str(kwargs):
    if kwargs:
        return '; '.join(f'{k}:{v}' for k, v in kwargs.items())
    else:
        return ''


def validate_columns(func):
    def wrapper(self, **kwargs):
        columns_list = kwargs.keys()
        if not all([k in self._columns for k in columns_list]):
            raise exceptions.KeyDoesntExists(f'One of given columns does not exists. Columns: {columns_list}')

        return func(self, **kwargs)

    return wrapper


class DBTable:

    def __init__(self, table_name, *columns):
        self.table_name = table_name
        self._db = []
        self._columns = ('entry_id', *columns)
        self._last_id = 1

        logger.info(f'Table created: "{self.table_name}". Columns: {", ".join(self._columns)}')

    @validate_columns
    def select(self, **kwargs):
        logger.info(f'Table: {self.table_name}. Select query with args: {kwargs_to_str(kwargs)}')

        resp = copy.deepcopy(self._db)
        for k, v in kwargs.items():
            resp = filter(lambda entry: entry.get(k) == v, resp)

        return list(resp)

    @validate_columns
    def insert(self, **kwargs):
        logger.info(f'Table: {self.table_name}. Insert query with args: {kwargs_to_str(kwargs)}')
        if 'entry_id' in kwargs:
            if kwargs['entry_id'] <= self._last_id:
                if len(self.select(id=kwargs['entry_id'])) > 0:
                    raise exceptions.EntryExists(f'Entry with id "{kwargs["entry_id"]}" already exists')
        else:
            kwargs['entry_id'] = self._last_id
        self._db.append(copy.deepcopy(kwargs))
        self._last_id += 1
        return kwargs

    @validate_columns
    def update(self, entry_id, **kwargs):
        all_kwargs = {"entry_id": entry_id}
        all_kwargs.update(kwargs)
        logger.info(f'Table: {self.table_name}. Update query with args: {kwargs_to_str(all_kwargs)}')
        for entry in self._db:
            if entry['entry_id'] == entry_id:
                for k, v in kwargs.items():
                    entry[k] = v

    def delete(self, entry_id):
        logger.info(f'Table: {self.table_name}. Delete query with args: entry_id: {entry_id}')
        self._db = [e for e in self._db if e['entry_id'] != entry_id]

    def truncate(self):
        logger.info(f'Table: {self.table_name}. Truncate table query')
        self._db = []
        self._last_id = 1

    @validate_columns
    def exists(self, **kwargs):
        logger.info(f'Table: {self.table_name}. Exists query with args: {kwargs_to_str(kwargs)}')
        return len(self.select(**kwargs)) > 0
