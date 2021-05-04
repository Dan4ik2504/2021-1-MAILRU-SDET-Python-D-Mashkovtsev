import utils
import settings


def most_frequent_requests(log_file_path=settings.LOG_FILE_NAME, limit=10):
    """
    Returns a list of URLs sorted by the number of requests

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    """
    items_list = utils.get_log_file_data_columns_by_name(log_file_path, settings.COLUMN_NAMES.URL, validate=False)
    items_count_dicts_list = utils.count_items_str_by_field(items_list, settings.COLUMN_NAMES.URL)

    answer = {
        "title": "Most frequent requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(most_frequent_requests, align_columns=False)
