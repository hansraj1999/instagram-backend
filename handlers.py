from database import get_db_pool
from asyncmy.cursors import DictCursor


class DatabaseHandler:
    def __init__(self):
        self.pool = None

    async def init(self):
        self.pool = await get_db_pool()

    async def execute(self, query: str, params: tuple = ()):
        """Execute a query (INSERT, UPDATE, DELETE) and commit."""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, params)
                await conn.commit()
                return cursor.lastrowid

    async def fetch_one(self, query: str, params: tuple = ()):
        """Fetch a single row."""
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchone()

    async def fetch_all(self, query: str, params: tuple = ()):
        """Fetch all rows."""
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cursor:
                await cursor.execute(query, params)
                return await cursor.fetchall()
