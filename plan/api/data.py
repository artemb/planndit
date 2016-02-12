from rest_framework import serializers


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
