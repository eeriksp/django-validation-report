import django.apps
from django.db.models import Model
from django.core.exceptions import ValidationError
from types import SimpleNamespace as Object


def compile_validation_report():
    """
    Run `full_clean` for all instances of Django models
    which have a custom `clean` function.
    """
    models = django.apps.apps.get_models()
    for model in models:
        if model.clean == Model.clean:
            continue
        for instance in model.objects.all():
            try:
                instance.full_clean()
            except ValidationError as e:
                yield _get_error_tuple(instance, e)


def _get_error_tuple(instance, error):
    result = Object()
    result.model_name = instance.__class__._meta.object_name
    result.instance = instance
    if isinstance(error, ValidationError):
        result.error_message = [message for message in error.error_dict['__all__']]
    else:
        result.error_message = error
    return result
