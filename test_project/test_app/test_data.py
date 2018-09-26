from django.contrib.auth.models import User
from .models import Person


def add_two_person_instances():
    monk_with_name = Person.objects.create(
        is_monastic=True,
        monastic_name='Lotus Jewel of Kindness'
    )
    monk_without_name = Person.objects.create(
        is_monastic=True
    )
