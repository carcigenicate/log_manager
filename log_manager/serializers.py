"""
For serialization and deserialization of the log data.

There are two formats: the input format, and the output format. Input data is in the form:

    {userId: ..., sessionId: ..., actions: [{time: ..., type: ..., properties: {...}]}

Whereas, responses are flat "actions" that have the user and session ID associated with each individually:

    [{time: ..., type: ..., properties: {...}, userId: ..., sessionId: ...}]
"""

from rest_framework import serializers

from log_manager.models import LogEntry


class InputLogActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ['time', 'type', 'properties']


class InputLogActionsSerializer(serializers.Serializer):
    userId = serializers.CharField()
    sessionId = serializers.CharField()
    actions = serializers.SerializerMethodField()

    def get_actions(self, obj):
        queryset = LogEntry.objects.filter(userId_id=obj.userId, sessionId_id=obj.sessionId)
        serializer = InputLogActionSerializer(queryset, many=True)
        return serializer.data


class OutputLogSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='userId.user_id')
    sessionId = serializers.CharField(source="sessionId.session_id")

    class Meta:
        model = LogEntry
        fields = ['time', 'type', 'properties', 'userId', 'sessionId']
