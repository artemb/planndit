from rest_framework import serializers

from plan.api.serializers import RouteSerializer


class Record(object):
    def __init__(self, success, message):
        self.success = success
        self.message = message

    class RecordSerializer(serializers.Serializer):
        success = serializers.BooleanField()
        message = serializers.CharField(max_length=255)

    @staticmethod
    def serialize(success, message=''):
        record = Record(success, message)
        return Record.RecordSerializer(record).data


class RouteRecord(object):
    def __init__(self, success, route):
        self.success = success
        self.route = route

    class RouteRecordSerializer(serializers.Serializer):
        success = serializers.BooleanField()
        route = RouteSerializer()

    @staticmethod
    def serialize(success, route):
        record = RouteRecord(success, route)
        return RouteRecord.RouteRecordSerializer(record).data