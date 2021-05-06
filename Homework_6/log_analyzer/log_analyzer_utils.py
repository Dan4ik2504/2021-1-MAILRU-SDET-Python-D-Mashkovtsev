import dataclasses
from typing import Union
from collections.abc import Iterable

from log_analyzer import settings


@dataclasses.dataclass
class LogItem:
    ip: str
    date_time: str
    method: str
    url: str
    http_version: str
    status_code: str
    size: int


@dataclasses.dataclass
class IncorrectLogItem:
    text: str


def is_valid_log_entry(entry_dict):
    """
    Validates log entry

    :param entry_dict: Dict with data
    """
    booleans = [
        len(entry_dict["method"]) <= 7,
        len(entry_dict["status_code"]) == 3,
        entry_dict["status_code"].isdigit(),
        entry_dict["size"].isdigit()
    ]
    return all(booleans)


def process_log_entry(entry: str):
    """
    Takes a string, processes it and returns a dictionary with the data contained in the string

    :param entry: String with data
    :return:
    """
    entry_list = entry.split(" ")
    entry_dict = {
        "ip": entry_list[0],
        "date_time": ' '.join(entry_list[3:5]).lstrip("[").rstrip("]"),
        "method": entry_list[5].lstrip('"'),
        "url": entry_list[6],
        "http_version": entry_list[7],
        "status_code": entry_list[8],
        "size": entry_list[9] if entry_list[9] != "-" else "0",
        "other": " ".join(entry_list[10:])
    }
    return entry_dict


def get_log_file_data_parsed(log_file_path: str, ignore_incorrect_log_data=True) \
        -> list[Union[LogItem, IncorrectLogItem]]:
    """
    Opens the log file, parses it and returns an objects of the each line.

    :param log_file_path: Log file path
    :param ignore_incorrect_log_data: If False, invalid lines will be written to the list as objects
    of class IncorrectLogItem. Default: True
    :return: List of objects of classes LogItem and IncorrectLogItem
    """
    items = []
    with open(log_file_path) as file:
        for line in file:
            entry_dict = process_log_entry(line)
            if is_valid_log_entry(entry_dict):
                item = LogItem(
                    ip=entry_dict["ip"],
                    date_time=entry_dict["date_time"],
                    method=entry_dict["method"],
                    url=entry_dict["url"],
                    http_version=entry_dict["http_version"],
                    status_code=entry_dict["status_code"],
                    size=int(entry_dict["size"])
                )
                items.append(item)
            else:
                if not ignore_incorrect_log_data:
                    item = IncorrectLogItem(text=line)
                    items.append(item)
    return items


def get_log_file_data_columns_by_name(log_file_path: str, column_name: str, validate=True):
    """
    Opens the log file, parses it and returns an list of strings with the values of the given column

    :param log_file_path: Log file path
    :param column_name: Name of the column
    :param validate: If True, the item will be checked before being added to the list
    :return: List of strings with the values of the given column
    """
    items = []
    with open(log_file_path) as file:
        for line in file:
            item_dict = process_log_entry(line)
            if validate:
                if is_valid_log_entry(item_dict):
                    items.append(item_dict[column_name])
            else:
                items.append(item_dict[column_name])
    return items


def count_items_objects_by_field(items_list: Iterable[LogItem], field_name: str):
    """
    Extracts a field_name from each item and counts the number of duplicate values.

    :param items_list: List of LogItem objects
    :param field_name: The name of the field whose values will be extracted and counted
    :return: List of dictionaries with fields 'count' and 'field_name'
    """
    items_list_str = [getattr(i, field_name) for i in items_list]
    items_count_dicts_list = count_items_str_by_field(items_list_str, field_name)
    return items_count_dicts_list


def count_items_str_by_field(items_list: Iterable[str], field_name: str):
    """
    Counts the number of duplicate values

    :param items_list: List of strings
    :param field_name: The name of the field. Used as the name of the entry in the dictionary
    :return: List of dictionaries with fields 'count' and 'field_name'
    """
    items_list = list(items_list)
    unique_items_list = list(dict.fromkeys(items_list))
    items_count_dicts_list = []
    for item in unique_items_list:
        items_count_dict = {
            field_name: item,
            "count": items_list.count(item)
        }
        items_count_dicts_list.append(items_count_dict)

    items_count_dicts_list = list(
        sorted(
            sorted(
                items_count_dicts_list,
                key=lambda i: i[field_name]
            ),
            key=lambda i: int(i[settings.COLUMN_NAMES.COUNT]),
            reverse=True
        )
    )

    return items_count_dicts_list
