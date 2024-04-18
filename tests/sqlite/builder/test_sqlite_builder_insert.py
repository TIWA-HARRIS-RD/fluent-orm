import inspect
import unittest

from tests.integrations.config.database import DATABASES
from src.fluentorm.connections import ConnectionFactory
from src.fluentorm.models import Model
from src.fluentorm.query import QueryBuilder
from src.fluentorm.query.grammars import SQLiteGrammar
from src.fluentorm.relationships import belongs_to
from tests.utils import MockConnectionFactory


class User(Model):
    __connection__ = "dev"
    __timestamps__ = False
    pass


class BaseTestQueryRelationships(unittest.TestCase):
    maxDiff = None

    def get_builder(self, table="users"):
        connection = ConnectionFactory().make("sqlite")
        return QueryBuilder(
            grammar=SQLiteGrammar,
            connection_class=connection,
            connection="dev",
            table=table,
            # model=User,
            connection_details=DATABASES,
        ).on("dev")

    def test_insert(self):
        builder = self.get_builder()
        result = builder.create(
            {"name": "Joe", "email": "joe@masoniteproject.com", "password": "secret"}
        )

        self.assertIsInstance(result["id"], int)
