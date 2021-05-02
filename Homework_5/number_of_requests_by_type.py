import utils
import settings


def number_of_requests_by_type(log_file_path=settings.LOG_FILE_NAME):
    """
    Number of requests by type

    :param log_file_path: Log file path
    """
    items_list = utils.get_log_file_data_columns_by_name(log_file_path, settings.COLUMN_NAMES.METHOD)
    items_count_dicts_list = utils.count_items_str_by_field(items_list, settings.COLUMN_NAMES.METHOD)

    answer = {
        "title": "Number of requests by type",
        "data": items_count_dicts_list
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(number_of_requests_by_type)