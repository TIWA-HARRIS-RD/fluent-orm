import inspect
import unittest

from tests.integrations.config.database import DATABASES
from src.fluentorm.connections import ConnectionFactory
from src.fluentorm.models import Model
from src.fluentorm.query import QueryBuilder
from src.fluentorm.query.grammars import SQLiteGrammar
from src.fluentorm.relationships import belongs_to
from tests.utils import MockConnectionFactory
from tests.integrations.config.database import DB
from src.fluentorm.collection import Collection


class User(Model):
    __connection__ = "dev"
    __timestamps__ = False


class BaseTestQueryRelationships(unittest.TestCase):
    maxDiff = None

    def get_builder(self, table="users"):
        connection = ConnectionFactory().make("sqlite")
        return QueryBuilder(
            grammar=SQLiteGrammar,
            connection="dev",
            table=table,
            model=User,
            connection_details=DATABASES,
        ).on("dev")

    def test_transaction(self):
        builder = self.get_builder()
        builder.begin()
        builder.create({"name": "phillip3", "email": "phillip3"})
        user = builder.where("name", "phillip3").first()
        self.assertEqual(user["name"], "phillip3")
        builder.rollback()
        user = builder.where("name", "phillip3").first()
        self.assertEqual(user, None)

    def test_transaction_globally(self):
        connection = DB.begin_transaction("dev")
        self.assertEqual(connection, self.get_builder().new_connection())
        DB.commit("dev")
        DB.begin_transaction("dev")
        DB.rollback("dev")

    def test_chunking(self):
        for users in self.get_builder().chunk(10):
            self.assertIsInstance(users, Collection)
