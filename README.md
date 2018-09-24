# Django Validation Report

Django Validation Report (DVR) allows you to control whether all model instances can be resaved without errors.

Suppose you have a Model:

```py
class Book(models.Model):
    is_published = models.BooleanField()
    publisher = models.CharField(max_length=100, blank=True)
```

Later on, after there are already some Books in the database, you add a `clean` method to the model:

```py
def clean(self):
    if self.is_published and not self.publisher:
        raise ValidationError('A published book must have a publisher specified')
```

Now, it would be nice to control whether the old Books meet new standards. Otherwise unexpected ValidationErrors might be risen if the old books are being resaved.

Django Validation Report offers a solution to this problem.

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

## Usage

Go to `/validation-report/` URL. You should see something like this:


># Validation report
>
>Run <i>full_clean()</i> for all Django model instances and return a report regarding failures.
>
>`Validating 'Book' with id '1' raised [ValidationError(["A published book must have a publisher specified"])]`
>
>`Validating 'Book' with id '3' raised [ValidationError(["A published book must have a publisher specified"])]`
>
>Task completed, 2  errors detected


If an error occurred and the server stopped delivering the `StreamingHttpResponse` before all model instances were checked, an error message will be shown:

># Validation report
>
>Run <i>full_clean()</i> for all Django model instances and return a report regarding failures.
>
>`Validating 'Book' with id '1' raised [ValidationError(["A published book must have a publisher specified"])]`
>
>
><h3 style="color: red;">ERROR: Task was not completed.</h3>