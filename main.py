import discord
import os
import random
import aiosqlite
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- POKEMON + IMAGE ----------------
POKEMON = {
    "Pikachu": "https://img.pokemondb.net/artwork/large/pikachu.jpg",
    "Eevee": "https://img.pokemondb.net/artwork/large/eevee.jpg",
    "Charmander": "https://img.pokemondb.net/artwork/large/charmander.jpg",
    "Bulbasaur": "https://img.pokemondb.net/artwork/large/bulbasaur.jpg",
    "Squirtle": "https://img.pokemondb.net/artwork/large/squirtle.jpg",
    "Dratini": "https://img.pokemondb.net/artwork/large/dratini.jpg",
    "Mew": "https://img.pokemondb.net/artwork/large/mew.jpg"
}

# ---------------- DB ----------------
async def setup():
    async with aiosqlite.connect("game.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS spawn(
            guild_id INTEGER PRIMARY KEY,
            name TEXT,
            shiny INTEGER
        )
        """)
        await db.commit()


@bot.event
async def on_ready():
    await setup()
    print(f"BOT ONLINE: {bot.user}")


# ---------------- SPAWN (WITH IMAGE) ----------------
@bot.command()
@commands.has_permissions(administrator=True)
async def spawn(ctx):

    name = random.choice(list(POKEMON.keys()))
    shiny = 1 if random.randint(1, 100) == 1 else 0

    async with aiosqlite.connect("game.db") as db:
        await db.execute(
            "INSERT OR REPLACE INTO spawn(guild_id,name,shiny) VALUES(?,?,?)",
            (ctx.guild.id, name, shiny)
        )
        await db.commit()

    embed = discord.Embed(
        title="🌿 Pokémon Muncul!",
        description=f"**{name}** muncul di alam liar!",
        color=0x00ff00 if not shiny else 0xffd700
    )

    embed.set_image(url=POKEMON[name])

    if shiny:
        embed.add_field(name="✨ SHINY!", value="Langka banget!")

    await ctx.send(embed=embed)


# ---------------- CATCH ----------------
@bot.command()
async def catch(ctx, *, name):

    async with aiosqlite.connect("game.db") as db:
        cur = await db.execute(
            "SELECT name,shiny FROM spawn WHERE guild_id=?",
            (ctx.guild.id,)
        )
        data = await cur.fetchone()

        if not data:
            return await ctx.send("Tidak ada Pokémon!")

        if data[0].lower() != name.lower():
            return await ctx.send("Salah Pokémon!")

        shiny = data[1]

        await db.execute("DELETE FROM spawn WHERE guild_id=?", (ctx.guild.id,))
        await db.commit()

    embed = discord.Embed(
        title="🎉 Pokémon Ditangkap!",
        description=f"{ctx.author.mention} menangkap **{name}**!",
        color=0xffd700 if shiny else 0x3498db
    )

    embed.set_image(url=POKEMON[name])

    if shiny:
        embed.add_field(name="✨ SHINY!", value="WOW LANGKA!")

    await ctx.send(embed=embed)


# ---------------- POKÉDEX ----------------
@bot.command()
async def dex(ctx, name):

    name = name.capitalize()

    if name not in POKEMON:
        return await ctx.send("Pokémon tidak ditemukan!")

    embed = discord.Embed(
        title=f"📖 Pokédex - {name}",
        description="Informasi Pokémon",
        color=0x2ecc71
    )

    embed.set_image(url=POKEMON[name])

    await ctx.send(embed=embed)


# ---------------- RUN ----------------
bot.run(TOKEN)
