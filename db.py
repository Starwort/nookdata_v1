from functools import wraps

import asyncpg


class Connection:
    conn: asyncpg.Connection

    @wraps(asyncpg.connect)
    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw

    async def __aenter__(self) -> asyncpg.Connection:
        self.conn = await asyncpg.connect(*self.args, **self.kw)
        return self.conn

    async def __aexit__(self, *_):
        await self.conn.close()
