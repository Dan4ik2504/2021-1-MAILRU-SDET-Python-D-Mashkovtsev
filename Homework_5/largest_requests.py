import utils
import settings


def largest_requests(log_file_path=settings.LOG_FILE_NAME, limit=5, remove_repeats=True):
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

    # items_list = [[i.url, i.status_code, i.size, i.ip] for i in items_list_sorted]
    if remove_repeats:
        items_list = []
        for i in items_list_sorted:
            dct = {
                "url": i.url,
                "status_code": i.status_code,
                "size": i.size,
                "ip": i.ip
            }
            if dct not in items_list:
                items_list.append(dct)
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
