from django.core.management.base import BaseCommand, CommandError
from validation_report.validation_report import compile_validation_report

class Command(BaseCommand):
    help = 'Checks whether all model instances can be resaved without errors'

    # def add_arguments(self, parser):
    #     parser.add_argument('--sendmail',
    #                         help='Send the report to addresses declared in django.conf.settings.MANAGERS')

    def handle(self, *args, **options):
            self.write('Run `full_clean()` for all Django model instances and return a report regarding failures.')
            report_len = 0
            for line in compile_validation_report():
                self.write(f"Validating '{line.model_name}' with id '{line.instance.id}' raised {line.error_message}")
                report_len += 1
            self.write(f'Task completed, {report_len} errors detected')
    
    def write(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))
