import discord
from discord.ext import commands

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="rank")
    async def rank(self, ctx):
        await ctx.send("📈 Rank system belum dikonfigurasi.")

    @commands.hybrid_command(name="leaderboard")
    async def leaderboard(self, ctx):
        await ctx.send("🏆 Leaderboard belum dikonfigurasi.")

    @commands.hybrid_command(name="setlevelreward")
    async def setlevelreward(self, ctx):
        await ctx.send("⚙️ Level rewards belum dikonfigurasi.")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
