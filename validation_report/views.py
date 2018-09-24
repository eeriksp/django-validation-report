from django.core.exceptions import PermissionDenied
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .validation_report import compile_validation_report
from .utils import get_obj_admin_change_url

RESPONSE_PRE = """<!DOCTYPE HTML>
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
"""
RESPONSE_POST = """
        </pre>
    </body>
</html>
"""


@login_required
def validation_report(request):
    return StreamingHttpResponse(_convert_to_html(compile_validation_report()))


def _convert_to_html(report):
    yield RESPONSE_PRE
    report_len = 0
    for line in report:
        report_len += 1
        # Try block is needed, because change URL exists only for models,
        # which have been added to admin directly, not as an inline
        try:
            id_display = get_obj_admin_change_url(line.instance, line.instance.id)
        except:
            id_display = line.instance.id
        yield f"<p>Validating <b>'{line.model_name}'</b> with id <b>'{id_display}'</b> raised {line.error_message}</p>"
    yield f'<h4 id="completed">Task completed, {report_len} errors detected</h4>'
    yield RESPONSE_POST
