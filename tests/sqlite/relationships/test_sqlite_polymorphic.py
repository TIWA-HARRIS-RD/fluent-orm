import os
import unittest

from src.fluentorm.models import Model
from src.fluentorm.relationships import belongs_to, has_many, morph_to
from tests.integrations.config.database import DB


class Profile(Model):
    __table__ = "profiles"
    __connection__ = "default"


class Articles(Model):
    __table__ = "articles"
    __connection__ = "default"

    @belongs_to("id", "article_id")
    def logo(self):
        return Logo


class Logo(Model):
    __table__ = "logos"
    __connection__ = "default"


class Like(Model):
    __connection__ = "default"

    @morph_to("record_type", "record_id")
    def record(self):
        return self


class User(Model):
    __connection__ = "default"

    _eager_loads = ()


DB.morph_map({"user": User, "article": Articles})


class TestRelationships(unittest.TestCase):
    maxDiff = None

    def test_can_get_polymorphic_relation(self):
        likes = Like.get()
        for like in likes:
            self.assertIsInstance(like.record, (Articles, User))

    def test_can_get_eager_load_polymorphic_relation(self):
        likes = Like.with_("record").get()
        for like in likes:
            self.assertIsInstance(like.record, (Articles, User))
