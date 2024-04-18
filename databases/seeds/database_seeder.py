"""Base Database Seeder Module."""

from src.fluentorm.seeds import Seeder
from .user_table_seeder import UserTableSeeder

class DatabaseSeeder(Seeder):

    def run(self):
        """Run the database seeds."""
        self.call(UserTableSeeder)
