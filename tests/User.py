""" User Model """

from src.fluentorm import Model


class User(Model):
    """User Model"""

    __fillable__ = ["name", "email", "password"]

    __connection__ = "sqlite"

    __auth__ = "email"

    __table__ = "users"

    @property
    def meta(self):
        return 1
