import discord
import os
import random
import aiosqlite
from discord.ext import commands

TOKEN = "TOKEN_BOT_KAMU_DISINI"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

STARTERS = ["Bulbasaur", "Charmander", "Squirtle"]

WILD_POKEMON = [
    "Pidgey", "Rattata", "Caterpie", "Weedle",
    "Zubat", "Pikachu", "Eevee", "Dratini"
]

# ---------------- DATABASE ----------------
async def setup_db():
    async with aiosqlite.connect("monster.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 500
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT,
            level INTEGER DEFAULT 5,
            iv INTEGER DEFAULT 50
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS spawns(
            guild_id INTEGER PRIMARY KEY,
            pokemon TEXT
        )
        """)

        await db.commit()


# ---------------- READY ----------------
@bot.event
async def on_ready():
    await setup_db()
    print(f"Bot online sebagai {bot.user}")


# ---------------- START ----------------
@bot.command()
async def start(ctx):
    async with aiosqlite.connect("monster.db") as db:
        cur = await db.execute("SELECT user_id FROM users WHERE user_id = ?", (ctx.author.id,))
        user = await cur.fetchone()

        if user:
            return await ctx.send("Kamu sudah daftar!")

        await db.execute("INSERT INTO users(user_id) VALUES(?)", (ctx.author.id,))
        await db.commit()

    await ctx.send("Daftar sukses! Ketik !pick untuk pilih starter.")


# ---------------- PICK STARTER ----------------
@bot.command()
async def pick(ctx, name):

    name = name.capitalize()

    if name not in STARTERS:
        return await ctx.send("Starter tidak valid!")

    async with aiosqlite.connect("monster.db") as db:

        cur = await db.execute("SELECT * FROM pokemon WHERE owner_id = ?", (ctx.author.id,))
        exist = await cur.fetchone()

        if exist:
            return await ctx.send("Kamu sudah punya starter!")

        iv = random.randint(40, 100)

        await db.execute(
            "INSERT INTO pokemon(owner_id,name,iv) VALUES(?,?,?)",
            (ctx.author.id, name, iv)
        )

        await db.commit()

    await ctx.send(f"Kamu memilih {name} dengan IV {iv}%!")


# ---------------- POKEMON LIST ----------------
@bot.command()
async def pokemon(ctx):

    async with aiosqlite.connect("monster.db") as db:
        cur = await db.execute("SELECT name,level,iv FROM pokemon WHERE owner_id = ?", (ctx.author.id,))
        data = await cur.fetchall()

    if not data:
        return await ctx.send("Kamu belum punya Pokémon.")

    msg = ""
    for p in data:
        msg += f"• {p[0]} Lv.{p[1]} IV:{p[2]}%\n"

    await ctx.send(msg)


# ---------------- SPAWN ----------------
@bot.command()
@commands.has_permissions(administrator=True)
async def spawn(ctx):

    poke = random.choice(WILD_POKEMON)

    async with aiosqlite.connect("monster.db") as db:
        await db.execute(
            "INSERT OR REPLACE INTO spawns(guild_id,pokemon) VALUES(?,?)",
            (ctx.guild.id, poke)
        )
        await db.commit()

    await ctx.send(f"🌿 Pokémon muncul! Ketik !catch {poke}")


# ---------------- CATCH ----------------
@bot.command()
async def catch(ctx, *, name):

    async with aiosqlite.connect("monster.db") as db:

        cur = await db.execute(
            "SELECT pokemon FROM spawns WHERE guild_id = ?",
            (ctx.guild.id,)
        )
        spawn = await cur.fetchone()

        if not spawn:
            return await ctx.send("Tidak ada Pokémon.")

        if spawn[0].lower() != name.lower():
            return await ctx.send("Salah Pokémon!")

        iv = random.randint(30, 100)

        await db.execute(
            "INSERT INTO pokemon(owner_id,name,iv) VALUES(?,?,?)",
            (ctx.author.id, name, iv)
        )

        await db.execute("DELETE FROM spawns WHERE guild_id = ?", (ctx.guild.id,))
        await db.commit()

    await ctx.send(f"🎉 {ctx.author.mention} menangkap {name} IV {iv}%!")


# ---------------- RUN ----------------
bot.run(TOKEN)