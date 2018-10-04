from django.core.mail import mail_admins
from .validation_report import compile_validation_report
from .utils import render_template

SUBJECT = 'Validation Report'

HTML_MESSAGE_TEMPLATE = """
<p>Dear Admins,<br>
By running <i>full_clean</i> for all Django model instances we detected the following errors:</p>
<ul>
{% for line in report %}
<li>Validating <b>'{{line.model_name}}'</b> with id <b>'{{line.id_display}}'</b> raised {{line.error_message}}</li>
{% endfor %}
</ul>
<p>In total, {{report_len}} errors were detected.</p>
<p>Wishing you a beautiful and serene day,<br>
your robot colleagues</p>
"""
MESSAGE_TEMPLATE = """
Dear Admins,\n\n
By running `full_clean` for all Django model instances we detected the following errors:\n
{% for line in report %}
  - Validating '{{line.model_name}}' with id '{{line.id_display}}' raised {{line.error_message}}\n
{% endfor %}
\nIn total, {{report_len}} errors were detected.\n\n
Wishing you a beautiful and serene day,\n
your robot colleagues
"""


def send_report_email(report):
    report_len = len(report)
    msg = _compile_message(MESSAGE_TEMPLATE, report, report_len)
    html_msg = _compile_message(HTML_MESSAGE_TEMPLATE, report, report_len)
    mail_admins(
        subject=SUBJECT,
        message=_compile_message(MESSAGE_TEMPLATE, report, report_len),
        html_message=_compile_message(
            HTML_MESSAGE_TEMPLATE, report, report_len),
    )


def _compile_message(template, report, report_len):
    context = {
        'report': report,
        'report_len': report_len,
    }
    return render_template(template, context)
