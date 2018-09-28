from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from validation_report.validation_report import compile_validation_report
from ...sendmail import send_report_email


class Command(BaseCommand):
    help = 'Checks whether all model instances can be resaved without errors'

    def add_arguments(self, parser):
        parser.add_argument('--sendmail',
                            action="store_true",
                            dest='sendmail',
                            help='Send the report to addresses declared in django.conf.settings.MANAGERS')

    def handle(self, *args, **options):
        self.write(
            'Run `full_clean()` for all Django model instances and return a report regarding failures.')
        report_len = 0
        report = compile_validation_report()
        for line in report:
            self.write(
                f"Validating '{line.model_name}' with id '{line.instance.id}' raised {line.error_message}")
            report_len += 1
        self.write(f'Task completed, {report_len} errors detected')

        if options['sendmail'] and report_len:
            send_report_email(report, report_len)
            recipients = '\n'.join([admin[1] for admin in settings.ADMINS])
            self.write("\nThe report was sent to the following addresses:\n"
                       f"{recipients}")

    def write(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))
