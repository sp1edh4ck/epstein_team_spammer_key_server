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

    async def bind_hardware(self, key, hardware_id):
        async with self.pool.acquire() as conn:
           return await conn.execute("UPDATE licenses SET hardware_id=$1 WHERE license_key=$2", hardware_id, key)
