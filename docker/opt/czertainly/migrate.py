import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CZERTAINLY_PyADCS_Connector.settings')
    from django.core.management import execute_from_command_line
    args = sys.argv + ["migrate", "PyADCSConnector"]
    execute_from_command_line(args)
