import environ
from django.db.backends.signals import connection_created
from django.dispatch import receiver

# Initialize environ
env = environ.Env()

@receiver(connection_created)
def set_search_path(sender, connection, **kwargs):
    """Set PostgreSQL search_path when a new DB connection is created."""
    database_schema = env("DATABASE_SCHEMA", default="pyadcs")  # Load from .env
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {database_schema};")
