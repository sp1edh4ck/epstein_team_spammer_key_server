from .db_engine import create_pool


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Создаёт пул подключений к PostgreSQL."""
        if self.pool is None:
            try:
                self.pool = await create_pool()
            except Exception as e:
                print(f"DB connection failed: {e}")
                raise

    async def get_license(self, key):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("SELECT * FROM licenses WHERE license_key=$1", key)

    async def set_hwid(self, key, hwid):
        async with self.pool.acquire() as conn:
           return await conn.execute("UPDATE licenses SET hwid=$1 WHERE license_key=$2", hwid, key)

    async def get_hwid(self, key):
        async with self.pool.acquire() as conn:
           return await conn.fetchval("SELECT hwid FROM licenses WHERE license_key=$1", key)
