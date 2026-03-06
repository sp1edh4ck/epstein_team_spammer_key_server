import asyncpg


async def create_pool():
    """Создаёт пул подключений к PostgreSQL."""
    return await asyncpg.create_pool(
        user='postgres',
        password='postgres',
        database='epstein_spammer',
        host='127.0.0.1',
        port='5432',
        min_size=2,
        max_size=10
    )
