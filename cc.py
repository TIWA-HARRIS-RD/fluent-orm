"""Sandbox experimental file used to quickly feature test features of the package
"""
import os

from src.fluentorm.query import QueryBuilder
from src.fluentorm.connections import MySQLConnection, PostgresConnection
from src.fluentorm.query.grammars import MySQLGrammar, PostgresGrammar
from src.fluentorm.models import Model
from src.fluentorm.relationships import has_many
import inspect


# builder = QueryBuilder(connection=PostgresConnection, grammar=PostgresGrammar).table("users").on("postgres")



# print(builder.where("id", 1).or_where(lambda q: q.where('id', 2).or_where('id', 3)).get())

class User(Model):
    __connection__ = "sqlite"
    __table__ = "users"
    __dates__ = ["verified_at"]

    @has_many("id", "user_id")
    def articles(self):
        return Article
class Article(Model):
    __connection__ = "sqlite"


# user = User.create({"name": "phill", "email": "phill"})
# print(inspect.isclass(User))
os.environ.setdefault("DB_CONFIG_PATH", "config/test-database")
#user = User.first()
#user.update({"verified_at": None, "updated_at": None})
print(User.all().serialize())

# print(user.serialize())
# print(User.first())