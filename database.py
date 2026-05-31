import aiosqlite

async def setup_database():
    async with aiosqlite.connect("monster.db") as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 1000
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT,
            level INTEGER DEFAULT 5,
            exp INTEGER DEFAULT 0
        )
        """)

        await db.commit()