from asyncmy import create_pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

DATABASE_URL = "mysql+aiomysql://test_user:test_password@127.0.0.1:3306/test_db" # TODO: put in env

# SQLAlchemy Base and metadata
Base = declarative_base()
metadata = MetaData()

# Database pool instance
db_pool = None

async def get_db_pool():
    global db_pool
    if not db_pool:
        db_pool = await create_pool(
            host="host.docker.internal",port=3306,user='test_user',
            password='test_password', db='test_db',
            maxsize=20
        )
    return db_pool
