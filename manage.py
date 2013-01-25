#!/usr/bin/env python
import os
import sys

from django.core.management import execute_from_command_line

from wger.main import get_user_config_path, setup_django_environment

if __name__ == "__main__":
    setup_django_environment(
        get_user_config_path('wger', 'settings.py'))
        
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wger.workout_manager.settings")

    execute_from_command_line(sys.argv)
