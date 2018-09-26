#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')
    try:
        from django.core.management import execute_from_command_line
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        print(BASE_DIR)
        sys.path.append(BASE_DIR)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
