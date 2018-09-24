from django.test import TestCase, Client
from django.urls import resolve

from validation_report.validation_report import compile_validation_report
from validation_report.views import validation_report, _convert_to_html
from .test_data import add_two_person_instances

RESPONSE_HTML = """<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="utf-8">
        <title>Validation report</title>
    </head>
    <body>
        <script>
            document.addEventListener('DOMContentLoaded', function(event) {
                var isCompleted = !!document.getElementById('completed');
                if (!isCompleted) {
                    var report = document.getElementById('report');
                    report.innerHTML += '<h3 style="color: red;">ERROR: Task was not completed.</h3>'
                }
            });
        </script>
        <h2>Validation report</h2>
        <h4>Run <i>full_clean()</i> for all Django model instances and return a report regarding failures.</h4>
        <pre id="report">
<p>Validating <b>'Person'</b> with id <b>'2'</b> raised [ValidationError(["If a Person is monastic, 'monastic_name' must be specified"])]</p><h4 id="completed">Task completed, 1 errors detected</h4>
        </pre>
    </body>
</html>
"""


class ValidationReportTest(TestCase):

    def test_url_resolves_to_validation_report_view(self):
        found = resolve('/validation-report/')  
        self.assertEqual(found.func, validation_report) 

    def test_validation_report(self):
        add_two_person_instances()
        response_generator = _convert_to_html(compile_validation_report())
        html = ''.join([line for line in response_generator])
        self.assertEqual(html, RESPONSE_HTML)

