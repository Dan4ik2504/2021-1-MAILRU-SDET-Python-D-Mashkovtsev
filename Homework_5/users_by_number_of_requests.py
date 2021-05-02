import utils
import settings


def users_by_number_of_requests(log_file_path=settings.LOG_FILE_NAME, limit=5):
    items = utils.get_log_file_data_parsed(log_file_path)
    items_list = []
    for item in items:
        if item.status_code.startswith("5"):
            items_list.append(item.ip)
    unique_items_list = list(set(items_list))
    items_count_dicts_list = []
    for item in unique_items_list:
        item_count_dict = {
            'ip': item,
            'count': items_list.count(item)
        }
        items_count_dicts_list.append(item_count_dict)

    items_count_dicts_list = list(
        sorted(items_count_dicts_list, key=lambda i: (int(i['count']), i['ip']), reverse=True)
    )

    answer = {
        "title": "Users by the number of requests",
        "data": items_count_dicts_list[:limit]
    }
    return answer


if __name__ == '__main__':
    utils.write_response_in_file(users_by_number_of_requests)