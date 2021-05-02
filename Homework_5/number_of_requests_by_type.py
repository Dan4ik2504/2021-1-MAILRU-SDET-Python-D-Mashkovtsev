import utils
import settings


def number_of_requests_by_type(log_file_path=settings.LOG_FILE_NAME):
    items_list = utils.get_log_file_data_columns_by_name(log_file_path, utils.ColumnNames.METHOD)
    unique_items_list = list(set(items_list))
    items_count_dicts_list = []
    for item in unique_items_list:
        item_count_dict = {
            'method': item,
            'count': items_list.count(item)
        }
        items_count_dicts_list.append(item_count_dict)

    items_count_dicts_list = list(
        sorted(items_count_dicts_list, key=lambda i: (int(i['count']), i['method']), reverse=True)
    )

    answer = {
        "title": "Number of requests by type",
        "data": items_count_dicts_list
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(number_of_requests_by_type)