import log_analyzer_utils
import settings


def number_of_requests(log_file_path=settings.LOG_FILE_PATH):
    """
    Total number of requests

    :param log_file_path: Log file path
    """
    with open(log_file_path) as file:
        answer = {
            "title": "Total number of requests",
            "data": len(file.readlines())
        }
        return answer


def number_of_requests_by_type(log_file_path=settings.LOG_FILE_PATH):
    """
    Number of requests by type

    :param log_file_path: Log file path
    """
    items_list = log_analyzer_utils.get_log_file_data_columns_by_name(log_file_path, settings.COLUMN_NAMES.METHOD)
    items_count_dicts_list = log_analyzer_utils.count_items_str_by_field(items_list, settings.COLUMN_NAMES.METHOD)

    answer = {
        "title": "Number of requests by type",
        "data": items_count_dicts_list
    }
    return answer


def most_frequent_requests(log_file_path=settings.LOG_FILE_PATH, limit=10):
    """
    Returns a list of URLs sorted by the number of requests

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    """
    items_list = log_analyzer_utils.get_log_file_data_columns_by_name(log_file_path, settings.COLUMN_NAMES.URL,
                                                                      validate=False)
    items_count_dicts_list = log_analyzer_utils.count_items_str_by_field(items_list, settings.COLUMN_NAMES.URL)

    answer = {
        "title": "Most frequent requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer


def largest_requests(log_file_path=settings.LOG_FILE_PATH, limit=5, remove_repeats=True):
    """
    Returns a list of requests sorted by size

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    :param remove_repeats: If true, repeats will be removed
    """
    all_items_list = log_analyzer_utils.get_log_file_data_parsed(log_file_path)

    items_list_sorted = list(
        sorted(
            sorted(
                filter(
                    lambda i: i.status_code.startswith('4'),
                    all_items_list
                ),
                key=lambda i: (i.url, i.status_code, i.ip)
            ),
            key=lambda i: int(i.size),
            reverse=True
        )
    )

    if remove_repeats:
        items_list = []
        for i in items_list_sorted:
            item_data_dict = {
                "url": i.url,
                "status_code": i.status_code,
                "size": i.size,
                "ip": i.ip
            }
            if item_data_dict not in items_list:
                items_list.append(item_data_dict)
            if len(items_list) >= limit:
                break
    else:
        items_list = [
            {
                "url": i.url,
                "status_code": i.status_code,
                "size": i.size,
                "ip": i.ip
            } for i in items_list_sorted[:limit]
        ]

    answer = {
        "title": "Largest requests",
        "data": items_list
    }
    return answer


def users_by_number_of_requests(log_file_path=settings.LOG_FILE_PATH, limit=5):
    """
    Returns a list of IPs sorted by the number of requests

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    """
    items_list = log_analyzer_utils.get_log_file_data_parsed(log_file_path)

    items_list = filter(lambda i: i.status_code.startswith("5"), items_list)
    items_count_dicts_list = log_analyzer_utils.count_items_objects_by_field(items_list, settings.COLUMN_NAMES.IP)

    answer = {
        "title": "Users by the number of requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer
