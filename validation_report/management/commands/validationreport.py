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
                            help='Send the report to addresses declared in django.conf.settings.ADMINS')

    def handle(self, *args, **options):
        self.write(
            'Run `full_clean()` for all Django model instances and return a report regarding failures.')
        report = []
        for line in compile_validation_report():
            report.append(line)
            self.write(
                f"Validating '{line.model_name}' with id '{line.instance.id}' raised {line.error_message}")
        self.write(f'Task completed, {len(report)} errors detected')

        if options['sendmail'] and report:
            send_report_email(report)
            recipients = '\n'.join([admin[1] for admin in settings.ADMINS])
            self.write("\nThe report was sent to the following addresses:\n"
                       f"{recipients}")

    def write(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))
