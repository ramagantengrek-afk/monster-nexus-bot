import discord
import os
import random
import aiosqlite
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

STARTERS = ["Bulbasaur", "Charmander", "Squirtle"]

WILD = ["Pidgey", "Rattata", "Pikachu", "Eevee", "Zubat"]

# ---------------- DATABASE ----------------
async def setup():
    async with aiosqlite.connect("pokemon.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS pokemon(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_id INTEGER,
            name TEXT,
            iv INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS spawn(
            guild_id INTEGER PRIMARY KEY,
            name TEXT
        )
        """)

        await db.commit()


# ---------------- READY ----------------
@bot.event
async def on_ready():
    await setup()
    print(f"BOT ONLINE: {bot.user}")


# ---------------- USER COMMAND ----------------
@bot.command()
async def start(ctx):
    async with aiosqlite.connect("pokemon.db") as db:
        cur = await db.execute("SELECT user_id FROM users WHERE user_id=?", (ctx.author.id,))
        if await cur.fetchone():
            return await ctx.send("Kamu sudah daftar!")

        await db.execute("INSERT INTO users(user_id) VALUES(?)", (ctx.author.id,))
        await db.commit()

    await ctx.send("Daftar sukses! ketik !pick")


@bot.command()
async def pick(ctx, name):
    name = name.capitalize()

    if name not in STARTERS:
        return await ctx.send("Starter tidak valid!")

    async with aiosqlite.connect("pokemon.db") as db:
        cur = await db.execute("SELECT * FROM pokemon WHERE owner_id=?", (ctx.author.id,))
        if await cur.fetchone():
            return await ctx.send("Kamu sudah punya Pokémon!")

        iv = random.randint(40, 100)

        await db.execute(
            "INSERT INTO pokemon(owner_id,name,iv) VALUES(?,?,?)",
            (ctx.author.id, name, iv)
        )
        await db.commit()

    await ctx.send(f"Kamu memilih {name} (IV {iv}%)")


@bot.command()
async def pokemon(ctx):
    async with aiosqlite.connect("pokemon.db") as db:
        cur = await db.execute("SELECT name,iv FROM pokemon WHERE owner_id=?", (ctx.author.id,))
        data = await cur.fetchall()

    if not data:
        return await ctx.send("Belum punya Pokémon!")

    msg = ""
    for p in data:
        msg += f"{p[0]} IV:{p[1]}%\n"

    await ctx.send(msg)


# ---------------- SPAWN (ADMIN) ----------------
@bot.command()
@commands.has_permissions(administrator=True)
async def spawn(ctx):

    poke = random.choice(WILD)

    async with aiosqlite.connect("pokemon.db") as db:
        await db.execute(
            "INSERT OR REPLACE INTO spawn(guild_id,name) VALUES(?,?)",
            (ctx.guild.id, poke)
        )
        await db.commit()

    await ctx.send(f"🌿 Pokémon muncul! ketik !catch {poke}")


# ---------------- CATCH ----------------
@bot.command()
async def catch(ctx, *, name):

    async with aiosqlite.connect("pokemon.db") as db:
        cur = await db.execute(
            "SELECT name FROM spawn WHERE guild_id=?",
            (ctx.guild.id,)
        )
        spawn = await cur.fetchone()

        if not spawn:
            return await ctx.send("Tidak ada Pokémon!")

        if spawn[0].lower() != name.lower():
            return await ctx.send("Salah Pokémon!")

        iv = random.randint(30, 100)

        await db.execute(
            "INSERT INTO pokemon(owner_id,name,iv) VALUES(?,?,?)",
            (ctx.author.id, name, iv)
        )

        await db.execute("DELETE FROM spawn WHERE guild_id=?", (ctx.guild.id,))
        await db.commit()

    await ctx.send(f"🎉 {ctx.author.mention} menangkap {name}!")


# ---------------- ADMIN COMMAND ----------------
@bot.command()
@commands.has_permissions(administrator=True)
async def give(ctx, member: discord.Member, *, pokemon_name):

    iv = random.randint(1, 100)

    async with aiosqlite.connect("pokemon.db") as db:
        await db.execute(
            "INSERT INTO pokemon(owner_id,name,iv) VALUES(?,?,?)",
            (member.id, pokemon_name, iv)
        )
        await db.commit()

    await ctx.send(f"Diberikan {pokemon_name} ke {member.name}")


@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx, member: discord.Member):

    async with aiosqlite.connect("pokemon.db") as db:
        await db.execute("DELETE FROM pokemon WHERE owner_id=?", (member.id,))
        await db.commit()

    await ctx.send(f"Pokémon {member.name} direset!")


# ---------------- RUN ----------------
bot.run(TOKEN)