from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from backend.infra.database.connection import DatabaseCORE

db_url = URL.create(drivername="sqlite", database="test.sqlite3")

test_engine = create_engine(db_url)


test_sync_session = sessionmaker(test_engine, autoflush=False, expire_on_commit=False)


test_core = DatabaseCORE(db_name="test.sqlite3", driver="sqlite+aiosqlite")
