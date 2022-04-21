from copy import deepcopy
import json

from django.test import TestCase, Client
from django.urls import reverse

from log_manager.models import LoggedUser, LoggedSession, LogEntry


class LogTestCaseBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.endpoint = reverse("api-list")

        self.post_kwargs = {"path": self.endpoint, "content_type": "application/json"}

        self.valid_data = {
            "userId": "ABC123XYZ",
            "sessionId": "XYZ456ABC",
            "actions": [
                {
                    "time": "2018-10-18T21:37:28-06:00",
                    "type": "CLICK",
                    "properties": {
                        "locationX": 52,
                        "locationY": 11
                    }
                },
                {
                    "time": "2020-10-18T21:37:30-06:00",
                    "type": "VIEW",
                    "properties": {
                        "viewedId": "FDJKLHSLD"
                    }
                }
            ]
        }

    def _post_valid(self):
        return self.client.post(**self.post_kwargs, data=self.valid_data)


class LogCreationTestCase(LogTestCaseBase):
    def setUp(self):
        super().setUp()

        self.invalid_container_data = deepcopy(self.valid_data)
        del self.invalid_container_data['userId']
        # Misspelled key
        self.invalid_container_data['useId'] = 'ABC123XYZ'

        self.invalid_action_data = deepcopy(self.valid_data)
        self.invalid_action_data['actions'][0]['time'] = "Invalid Time"

    def test_valid_creation(self):
        response = self._post_valid()

        self.assertEqual(response.status_code, 201)

        users = LoggedUser.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(users[0].user_id, self.valid_data['userId'])

        log_entries = LogEntry.objects.all()
        self.assertEqual(log_entries.count(), 2)
        self.assertEqual(log_entries[0].userId.user_id, self.valid_data['userId'])

        session_entries = LoggedSession.objects.all()
        self.assertEqual(session_entries.count(), 1)
        self.assertEqual(session_entries[0].session_id, self.valid_data['sessionId'])

    def _assert_nothing_created(self):
        self.assertEqual(LoggedUser.objects.count(), 0)
        self.assertEqual(LoggedSession.objects.count(), 0)
        self.assertEqual(LogEntry.objects.count(), 0)

    def test_invalid_container_key_creation(self):
        response = self.client.post(**self.post_kwargs, data=self.invalid_container_data)

        self.assertEqual(response.status_code, 400)

        errors = json.loads(response.content)
        container_errors = errors.get('container_errors')
        self.assertEqual(container_errors, {'userId': ['This field is required.']})
        self._assert_nothing_created()

    def test_invalid_action_value_creation(self):
        response = self.client.post(**self.post_kwargs, data=self.invalid_action_data)

        self.assertEqual(response.status_code, 400)
        errors = json.loads(response.content)
        action_errors = errors.get('action_errors')
        self.assertEqual(action_errors, [{'time': ['Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].']}])
        self._assert_nothing_created()


class LogListTestCase(LogTestCaseBase):
    def test_basic_retrieval(self):
        self._post_valid()

        response = self.client.get(self.endpoint)

        parsed = json.loads(response.content)

        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]['userId'], self.valid_data['userId'])
        self.assertEqual(parsed[0]['sessionId'], self.valid_data['sessionId'])

    def test_filtered_retrieval(self):
        self._post_valid()

        response = self.client.get(self.endpoint, {"start_time": "2019-01-01"})

        parsed = json.loads(response.content)

        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['properties']['viewedId'], "FDJKLHSLD")