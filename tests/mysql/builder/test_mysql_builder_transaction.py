import inspect
import os
import unittest

from src.fluentorm.connections import ConnectionFactory
from src.fluentorm.models import Model
from src.fluentorm.query import QueryBuilder
from src.fluentorm.query.grammars import MySQLGrammar
from src.fluentorm.relationships import belongs_to
from tests.utils import MockConnectionFactory
from tests.integrations.config.database import DB

if os.getenv("RUN_MYSQL_DATABASE") == "True":

    class User(Model):
        __connection__ = "mysql"
        __timestamps__ = False

    class BaseTestQueryRelationships(unittest.TestCase):
        maxDiff = None

        def get_builder(self, table="users"):
            connection = ConnectionFactory().make("mysql")
            return QueryBuilder(
                grammar=MySQLGrammar, connection=connection, table=table
            ).on("mysql")

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

        def test_transaction_default_globally(self):
            connection = DB.begin_transaction()
            self.assertEqual(connection, self.get_builder().new_connection())
            DB.commit()
            DB.begin_transaction()
            DB.rollback()
