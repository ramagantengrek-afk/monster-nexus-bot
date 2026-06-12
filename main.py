import discord
from discord.ext import commands
import os
import asyncio
from config import TOKEN, DEFAULT_PREFIX

class PokemonBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=DEFAULT_PREFIX, intents=intents)

    async def setup_hook(self):
        # Load cogs
        cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"Loaded extension: {filename}")
                except Exception as e:
                    print(f"Failed to load extension {filename}: {e}")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

if __name__ == "__main__":
    bot = PokemonBot()
    bot.run(TOKEN)
    