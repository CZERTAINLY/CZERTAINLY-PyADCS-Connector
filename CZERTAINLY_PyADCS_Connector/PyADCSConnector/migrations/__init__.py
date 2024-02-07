from typing import Any

import environ
from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import pre_migrate
from django.dispatch import receiver

env = environ.Env()

import logging

logger = logging.getLogger(__name__)


@receiver(pre_migrate)
def create_schema(sender: AppConfig, **kwargs: Any) -> None:
    with connection.cursor() as cursor:
        logger.info("Checking if schema should be created")
        sql_command = "CREATE SCHEMA IF NOT EXISTS " + env("DATABASE_SCHEMA") + ";"
        cursor.execute(sql_command)
