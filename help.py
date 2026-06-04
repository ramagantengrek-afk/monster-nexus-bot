import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        description="Show all Dupa Bot commands"
    )
    async def help(self, ctx):

        embed = discord.Embed(
            title="📖 Dupa Bot Help",
            description="List of available commands",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🛡️ Moderation",
            value="""
`/warn`
`/warnings`
`/timeout`
`/kick`
`/ban`
`/purge`
`/lock`
`/unlock`
            """,
            inline=False
        )

        embed.add_field(
            name="👋 Welcome",
            value="""
`/setwelcome`
`/setleave`
`/setautorole`
            """,
            inline=False
        )

        embed.add_field(
            name="🎫 Tickets",
            value="""
`/ticket setup`
`/ticket close`
`/ticket add`
`/ticket remove`
            """,
            inline=False
        )

        embed.add_field(
            name="🎁 Giveaways",
            value="""
`/gstart`
`/gend`
`/greroll`
            """,
            inline=False
        )

        embed.add_field(
            name="📈 Leveling",
            value="""
`/rank`
`/leaderboard`
`/setlevelreward`
            """,
            inline=False
        )

        embed.add_field(
            name="💰 Economy",
            value="""
`/balance`
`/daily`
`/work`
`/shop`
`/buy`
`/inventory`
`/pay`
            """,
            inline=False
        )

        embed.add_field(
            name="🎭 Roles",
            value="""
`/rolepanel`
`/reactionroles`
            """,
            inline=False
        )

        embed.add_field(
            name="⚙️ Utility",
            value="""
`/ping`
`/avatar`
`/banner`
`/userinfo`
`/serverinfo`
            """,
            inline=False
        )

        embed.set_footer(
            text="Dupa Bot • Advanced Discord Management"
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))