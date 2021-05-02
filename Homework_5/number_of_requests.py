from utils import write_response_in_file
import settings


def number_of_requests(log_file_path=settings.LOG_FILE_NAME):
    with open(log_file_path) as file:
        answer = {
            "title": "Total number of requests",
            "data": len(file.readlines())
        }
        return answer


if __name__ == '__main__':
    write_response_in_file(number_of_requests)
