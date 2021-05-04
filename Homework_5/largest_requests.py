import utils
import settings


def largest_requests(log_file_path=settings.LOG_FILE_NAME, limit=5, remove_repeats=True):
    """
    Returns a list of requests sorted by size

    :param log_file_path: Log file path
    :param limit: Maximum number of objects to return
    :param remove_repeats: If true, repeats will be removed
    """
    all_items_list = utils.get_log_file_data_parsed(log_file_path)

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


if __name__ == '__main__':
    utils.write_response_in_file(largest_requests, align_columns=False)
