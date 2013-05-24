from django.db import connection
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        """
        Do actual database drop.
        """
        cursor = connection.cursor()
        drop_command = "DROP DATABASE %s;"%(connection.settings_dict['NAME'],)
        self.stdout.write("Executing: %s"%(drop_command,))
        cursor.execute(drop_command)
        recreate_command = "CREATE DATABASE %s;"%(connection.settings_dict['NAME'])
        self.stdout.write("Executing: %s"%(recreate_command,))
        cursor.execute(recreate_command)
