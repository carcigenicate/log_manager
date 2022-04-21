from django.db import models


class LoggedUser(models.Model):
    user_id = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id


class LoggedSession(models.Model):
    session_id = models.CharField(max_length=10)

    def __str__(self):
        return self.session_id


class LogEntry(models.Model):
    time = models.DateTimeField()

    # If there's a closed-set of types, this would benefit from including a models.TextChoices "enum"
    # The sample is insufficient to determine that though.
    type = models.CharField(max_length=50)

    # There does not seem to be a consistent "shape" to the property data, so storing it as raw JSON seems appropriate.
    properties = models.JSONField()

    userId = models.ForeignKey(LoggedUser, on_delete=models.SET_NULL, null=True, related_name="actions")

    sessionId = models.ForeignKey(LoggedSession, on_delete=models.SET_NULL, null=True, related_name="actions")



