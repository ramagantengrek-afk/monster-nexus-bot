import discord
import os
from discord.ext import commands

# TOKEN dari Railway/GitHub ENV
TOKEN = os.getenv("DISCORD_TOKEN")

# ID Pokétwo
POKETWO_ID = 716390085896962058

# ID ROLE yang mau di ping (Pokémon Hunter)
ROLE_ID = 123456789012345678  # ganti nanti

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot online sebagai {bot.user}")

@bot.event
async def on_message(message):

    # cek apakah pesan dari Pokétwo
    if message.author.id == POKETWO_ID:

        # cek embed spawn
        if message.embeds:
            embed = message.embeds[0]

            if embed.title and "wild pokémon has appeared" in embed.title.lower():
                
                # kirim notifikasi
                await message.channel.send(f"<@&{ROLE_ID}> ⚡ Pokémon muncul di spawn!")

    await bot.process_commands(message)

bot.run(TOKEN)