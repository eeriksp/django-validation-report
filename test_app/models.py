from django.db import models
from django.core.exceptions import ValidationError


class Person(models.Model):
    is_monastic = models.BooleanField()
    monastic_name = models.CharField(max_length=100, blank=True)

    def clean(self):
        if self.is_monastic and not self.monastic_name:
            raise ValidationError(
                "If a Person is monastic, 'monastic_name' must be specified")
