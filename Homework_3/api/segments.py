import allure

import settings
from api import settings_api
from api.client import ApiClient


class NewSegment:
    name: str = None

    def __init__(self, segments_api):
        self.segments_api = segments_api

    def generate_json(self):
        """Creates data for a request in the form of a dictionary, which is serializable in JSON"""
        json = {
            'name': self.name,
            'pass_condition': 1,
            'relations': [
                {
                    'object_type': 'remarketing_player',
                    'params': {
                        'type': 'positive',
                        'left': 365,
                        'right': 0}
                }
            ],
            'logicType': 'or'
        }
        return json

    @allure.step("Segment saving")
    def save(self):
        """Sends a request to save a new campaign"""
        json = self.generate_json()
        self.segments_api.post_request(settings.Url.Api.SEGMENTS, json=json)
        self.segments_api.logger.info(f'Segment saved. Name: "{self.name}"')


class Segment:
    def __init__(self, data_dict, segments_api):
        self.segments_api = segments_api
        self.id = data_dict["id"]
        self.name = data_dict["name"]

    @allure.step("Segment deletion")
    def delete(self):
        """Sends a request to delete a segment"""
        self.segments_api.delete_request(settings.Url.Api.SEGMENT_BY_ID.format(id=self.id), expected_status=204,
                                         jsonify=False)
        self.segments_api.logger.info(f'Segment "{str(self)}" deleted')

    def __eq__(self, other):
        if other.isdigit() or isinstance(other, int):
            return self.id == int(other)
        else:
            return self.name == str(other)

    def __repr__(self):
        return f'{self.id}-{self.name}'


class SegmentsApi(ApiClient):

    class Exceptions(ApiClient.Exceptions):
        class SegmentNotExists(Exception):
            pass

    @allure.step("Searching for segments")
    def get_all_segments(self):
        """Returns all segments"""
        self.logger.info("Searching for segments")
        params = {
            "fields": ','.join(["id", "name"]),
            "sorting": "-id"
        }
        segments_dicts = self.get_request(settings.Url.Api.SEGMENTS, params=params)["items"]

        segments = []
        for segment_dict in segments_dicts:
            segment = Segment(segment_dict, self)
            segments.append(segment)

        self.logger.info(f'{len(segments_dicts)} segments exists')
        self.logger.debug(f'There are {len(segments_dicts)} segments: '
                          f'"{"; ".join([str(c) for c in segments_dicts])}"')

        return segments

    def get_new_segment_object(self):
        """Returns new segment"""
        return NewSegment(self)

    def get_segment_by_name(self, segment_name):
        """Returns segment found by the given name"""
        segments = self.get_all_segments()
        for segments in segments:
            if segments.name == segment_name:
                return segments
        raise self.Exceptions.SegmentNotExists(f'Segment with name "{segment_name}" does not exists')
