from django.db import models


class LoggedUser(models.Model):
    user_id = models.CharField(max_length=10)


class LogEntry(models.Model):
    time = models.DateTimeField()

    # If there's a closed-set of types, this would benefit from including a models.TextChoices "enum"
    # The sample is insufficient to determine that though.
    type = models.CharField(max_length=50)

    # There does not seem to be a consistent "shape" to the property data, so storing it as raw JSON seems appropriate.
    properties = models.JSONField()

    user = models.ForeignKey(LoggedUser, on_delete=models.SET_NULL, null=True)


class LoggedSession(models.Model):
    session_id = models.CharField(max_length=10)

    user = models.ForeignKey(LoggedUser, on_delete=models.SET_NULL, null=True)