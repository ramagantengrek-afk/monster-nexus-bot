import discord
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="gstart")
    async def gstart(self, ctx):
        await ctx.send("🎉 Giveaway started!")

    @commands.hybrid_command(name="gend")
    async def gend(self, ctx):
        await ctx.send("🏁 Giveaway ended!")

    @commands.hybrid_command(name="greroll")
    async def greroll(self, ctx):
        await ctx.send("🔄 Giveaway rerolled!")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
