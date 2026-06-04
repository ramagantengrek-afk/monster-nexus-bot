from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kick(self, ctx, member, *, reason=None):
        pass

    @commands.command()
    async def ban(self, ctx, member, *, reason=None):
        pass

    @commands.command()
    async def warn(self, ctx, member, *, reason=None):
        pass

async def setup(bot):
    await bot.add_cog(
        Moderation(bot)
    )