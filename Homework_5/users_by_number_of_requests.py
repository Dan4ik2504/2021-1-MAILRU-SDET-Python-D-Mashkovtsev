import utils
import settings


def users_by_number_of_requests(log_file_path=settings.LOG_FILE_NAME, limit=5):
    """
    Returns a list of IPs sorted by the number of requests

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    """
    items_list = utils.get_log_file_data_parsed(log_file_path)

    items_list = filter(lambda i: i.status_code.startswith("5"), items_list)
    items_count_dicts_list = utils.count_items_objects_by_field(items_list, settings.COLUMN_NAMES.IP)

    answer = {
        "title": "Users by the number of requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(users_by_number_of_requests)