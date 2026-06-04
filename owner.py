from discord.ext import commands
from config import OWNER_ID

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(ctx):
        return ctx.author.id == OWNER_ID

    @commands.command()
    @commands.check(is_owner)
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Owner(bot))