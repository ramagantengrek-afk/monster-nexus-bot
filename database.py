import aiosqlite

DATABASE = "data/bot.db"

async def setup_database():

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS guilds(
            guild_id INTEGER PRIMARY KEY
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS economy(
            guild_id INTEGER,
            user_id INTEGER,
            balance INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS levels(
            guild_id INTEGER,
            user_id INTEGER,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings(
            guild_id INTEGER,
            user_id INTEGER,
            warns INTEGER DEFAULT 0
        )
        """)

        await db.commit()