import utils
import settings


def most_frequent_requests(log_file_path=settings.LOG_FILE_NAME, limit=10):
    items_list = utils.get_log_file_data_columns_by_name(log_file_path, utils.ColumnNames.URL, validate=False)
    unique_items_list = list(set(items_list))
    items_count_dicts_list = []
    for item in unique_items_list:
        items_count_dict = {
            "url": item,
            "count": items_list.count(item)
        }
        items_count_dicts_list.append(items_count_dict)

    items_count_dicts_list = list(
        sorted(items_count_dicts_list, key=lambda i: (int(i['count']), i['url']), reverse=True)
    )

    answer = {
        "title": "Most frequent requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(most_frequent_requests, align_columns=False)
