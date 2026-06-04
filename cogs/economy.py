from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def balance(self, ctx):
        pass

    @commands.command()
    async def daily(self, ctx):
        pass

    @commands.command()
    async def work(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(
        Economy(bot)
    )