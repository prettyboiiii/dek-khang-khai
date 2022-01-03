from src.utils.configs.app_settings import get_settings
from pony.orm import Database
import logging
import time

class PonyORMService():
    def __init__(self) -> None:
        self.db = Database()
        self.attempts = 0
        self.max_retries = 5
        self.is_open = False

    def migrate(self, db: Database) -> None:
        try:
            db.generate_mapping(create_tables=True)
            logging.info('Migrated Database')
        except Exception as e:
            logging.error(e)

    def start(self) -> Database:
        while not(self.is_open):
            self.attempts += 1
            try:
                # PostgreSQL
                db_setting = {
                    "provider":get_settings().DBMS,
                    "user":get_settings().DB_USER,
                    "password":get_settings().DB_PASSWORD,
                    "host":get_settings().DB_HOST,
                    "database":get_settings().DB_DATABASE,
                    "port":get_settings().DB_PORT,
                }
                self.db.bind(**db_setting)
                is_open = True
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                logging.error(e)
                logging.info(f"Retry connection (#{self.attempts}) to database. Please check the connection to database.")
                if self.max_retries < self.attempts:
                    logging.info(f"Max attempts reached {self.attempts}. Raise error instead of retry. Please check the connection to database")
                    raise
                time.sleep(min(self.attempts * 2, 30))

        return self.db