import inspect
import os
import unittest

from tests.integrations.config.database import DATABASES
from src.fluentorm.connections import ConnectionFactory
from src.fluentorm.models import Model
from src.fluentorm.query import QueryBuilder
from src.fluentorm.query.grammars import PostgresGrammar
from src.fluentorm.relationships import belongs_to
from tests.utils import MockConnectionFactory

if os.getenv("RUN_POSTGRES_DATABASE") == "True":

    class User(Model):
        __connection__ = "postgres"
        __timestamps__ = False

    class BaseTestQueryRelationships(unittest.TestCase):
        maxDiff = None

        def get_builder(self, table="users"):
            connection = ConnectionFactory().make("postgres")
            return QueryBuilder(
                grammar=PostgresGrammar,
                connection=connection,
                table=table,
                # model=User,
                connection_details=DATABASES,
            ).on("postgres")

        def test_transaction(self):
            builder = self.get_builder()
            builder.begin()
            builder.create({"name": "phillip2", "email": "phillip2"})
            # builder.commit()
            user = builder.where("name", "phillip2").first()
            self.assertEqual(user["name"], "phillip2")
            builder.rollback()
            user = builder.where("name", "phillip2").first()
            self.assertEqual(user, None)
