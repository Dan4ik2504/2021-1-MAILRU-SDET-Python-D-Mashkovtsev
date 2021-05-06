from database import models


class DBBuilder:

    def __init__(self, client):
        self.client = client

    def create_entry_number_of_requests(self, count):
        entry = models.NumberOfRequests(count=count)
        self.client.session.add(entry)
        return entry

    def create_entry_number_of_requests_by_type(self, method, count):
        entry = models.NumberOfRequestsByType(method=method, count=count)
        self.client.session.add(entry)
        return entry

    def create_entry_most_frequent_requests(self, url, count):
        entry = models.MostFrequentRequests(url=url, count=count)
        self.client.session.add(entry)
        return entry

    def create_entry_largest_requests(self, url, status_code, size, ip):
        entry = models.LargestRequests(url=url, status_code=status_code, size=size, ip=ip)
        self.client.session.add(entry)
        return entry

    def create_entry_users_by_number_of_requests(self, ip, count):
        entry = models.UsersByNumberOfRequests(ip=ip, count=count)
        self.client.session.add(entry)
        return entry
