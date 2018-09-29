# Django Validation Report

Django Validation Report (DVR) allows you to control whether all model instances can be resaved without errors.

Suppose you have a Model:

```py
class Person(models.Model):
    is_monastic = models.BooleanField()
    monastic_name = models.CharField(max_length=100, blank=True)
```

Later on, after there are already some Person objects in the database, you add a `clean` method to the model:

```py
    def clean(self):
        if self.is_monastic and not self.monastic_name:
            raise ValidationError(
                "If a Person is monastic, 'monastic_name' must be specified")
```

Now, it would be nice to control whether the old Person objects meet new standards. Otherwise unexpected ValidationErrors might be risen if the old ones are being resaved.

Django Validation Report offers a solution to this problem.

## Features

DVR provides:

1. a report view for logged in users
2. a `manage.py` command to show the report on the console
3. automatic report email sending to admins; this is designed to be addded to your CI/CD script

## Requirements

- Python 3
- Django 2 (should aslo work with previous versions, but it hasn't been tested. See issue [#1](https://github.com/eeriksp/django-validation-report/issues/1))

## Installation

Install using pip:

```
pip install django-validation-report
```

Then add `validation_report` to your INSTALLED_APPS.

```py
INSTALLED_APPS = [
    ...
    'validation_report.apps.ValidationReportConfig',
]
```

To your main `urls.py` add:

```py
urlpatterns = [
    ...
    path('validation-report/', include('validation_report.urls')),
]
```

Also make sure you have specified `LOGIN_URL` in your `settings.py`. In order to see the generated report, the user must be logged in. If you do not have a custom login page, you can just use the default admin login page `LOGIN_URL = '/admin/login/'`.

The emails are sent to `settings.ADMINS`, so check that this constant has been specified and email sending has been configured.

## Usage

### View

Go to `/validation-report/` URL. As a logged in user, you should see something like this:

```
Validation report

Run full_clean() for all Django model instances and return a report regarding failures.

Validating 'Person' with id '1' raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]
Validating 'Person' with id '3' raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]

Task completed, 2  errors detected
```


If an error occurred and the server stopped delivering the `StreamingHttpResponse` before all model instances were checked, an error message will be shown:

```
Validation report

Run full_clean() for all Django model instances and return a report regarding failures.

Validating 'Person' with id '1' raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]

ERROR: Task was not completed, server response was interrupted.
```

### `Manage.py` command

Type

```
$ ./manage.py validationreport
```
The given report is similar to the one returned by the view in the previous chapter.

### Email sending

Type

```
$ ./manage.py validationreport --sendmail
```
You should see something like this:

```
Run `full_clean()` for all Django model instances and return a report regarding failures.
Validating 'Person' with id '1' raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]
Validating 'Person' with id '3' raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]
Task completed, 2  errors detected

The report was sent to the following addresses:
abbot@monastery.eu
```

This command is especially useful for adding to your CI/CD script, so you will be notified on time and all possible confusion can be avoided.

## License

DVR is published under MIT license.

Inspired by [SQLite developers](https://www.sqlite.org/different.html), we add the following blessing:

>May you do good and not evil\
May you find forgiveness for yourself and forgive others\
May you share freely, never taking more than you give.