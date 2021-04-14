import allure

import settings
from api import settings_api
from api.client import ApiClient


class NewSegment:
    name: str = None

    def __init__(self, segments_api):
        self.segments_api = segments_api

    def generate_json(self):
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
        self.segments_api.logger.info(f'Segment saving. Name: "{self.name}"')
        json = self.generate_json()
        self.segments_api.post_request(settings.Url.Api.SEGMENTS, json=json)


class Segment:
    def __init__(self, data_dict, segments_api):
        self.segments_api = segments_api
        self.id = data_dict["id"]
        self.name = data_dict["name"]

    def delete(self):
        self.segments_api.delete_request(settings.Url.Api.SEGMENT_BY_ID.format(id=self.id), expected_status=204,
                                         jsonify=False)

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

    def get_all_segments(self):
        params = {
            "fields": ','.join(["id", "name"]),
            "sorting": "-id"
        }
        response = self.get_request(settings.Url.Api.SEGMENTS, params=params)

        segments = []
        for segm_data in response["items"]:
            segment = Segment(segm_data, self)
            segments.append(segment)

        return segments

    def get_new_segment_object(self):
        return NewSegment(self)

    def get_segment_by_name(self, segment_name):
        segments = self.get_all_segments()
        for segments in segments:
            if segments.name == segment_name:
                return segments
        raise self.Exceptions.SegmentNotExists(f'Segment with name "{segment_name}" does not exists')
