from rest_framework import viewsets
from rest_framework.response import Response

from log_manager.models import LogEntry, LoggedUser, LoggedSession
from log_manager.serializers import InputLogActionSerializer, InputLogActionsSerializer, OutputLogSerializer


class LogViewSet(viewsets.ViewSet):
    def create(self, request):
        # Deserializes the outer "container" that wraps the actions
        container_serializer = InputLogActionsSerializer(data=request.data)

        # Deserializes the list of provided actions.
        actions_serializer = InputLogActionSerializer(data=request.data.get('actions'), many=True)

        # Not inlining these checks into the condition since both "is_valid"s **must** be called in order to generate
        #   the error response in the event of failure.
        container_is_valid = container_serializer.is_valid()
        actions_are_valid = actions_serializer.is_valid()
        if container_is_valid and actions_are_valid:
            container_data = container_serializer.validated_data
            actions_data = actions_serializer.validated_data

            # Ensure there are records for both the user and session so they can be tracked.
            user_id = container_data['userId']
            session_id = container_data['sessionId']
            user, _ = LoggedUser.objects.get_or_create(user_id=user_id)
            session, _ = LoggedSession.objects.get_or_create(session_id=session_id)

            action_instances = [LogEntry(time=action['time'],
                                         type=action['type'],
                                         properties=action['properties'],
                                         userId=user,
                                         sessionId=session)
                                for action in actions_data]

            LogEntry.objects.bulk_create(action_instances)
            return Response(status=201)
        else:
            errors = {"container_errors": container_serializer.errors,
                      "action_errors": [error for error in actions_serializer.errors if error]}
            return Response(errors, status=400)

    def list(self, request):
        queryset = LogEntry.objects.all()

        # This could be cleaned up by doing inline assignments using :=. This requires a fairly recent version of Python
        #  though, so I'm refraining from using it since I don't know what version this will be run with.
        user = request.query_params.get('user')
        log_type = request.query_params.get('type')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        # Direct boolean tests are only safe if falsey values will never be valid! Must use "is not None" otherwise.
        if user:
            queryset = queryset.filter(userId__user_id=user)

        if log_type:
            queryset = queryset.filter(type=log_type)

        if start_time:
            queryset = queryset.filter(time__gte=start_time)

        # Exclusive end bound!
        if end_time:
            queryset = queryset.filter(time__lt=end_time)

        serializer = OutputLogSerializer(queryset, many=True)
        return Response(serializer.data)