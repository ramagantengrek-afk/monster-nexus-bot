import discord
from discord.ext import commands
from ..utils.database import get_db_connection

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pokemon")
    async def list_pokemon(self, ctx):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pokemons WHERE owner_id = ?', (ctx.author.id,))
        pokemons = cursor.fetchall()
        conn.close()

        if not pokemons:
            return await ctx.send("You don't have any Pokémon yet!")

        description = ""
        for p in pokemons:
            description += f"ID: {p['id']} | **{p['name']}** (Lvl {p['level']})\n"
        
        embed = discord.Embed(title=f"{ctx.author.name}'s Pokémon", description=description)
        await ctx.send(embed=embed)

    @commands.command(name="bal")
    async def balance(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        conn.close()
        
        balance = row['balance'] if row else 0
        await ctx.send(f"{user.mention} has **{balance} coins**.")

    @commands.command()
    async def info(self, ctx, pokemon_id: int = None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if pokemon_id:
            cursor.execute('SELECT * FROM pokemons WHERE id = ? AND owner_id = ?', (pokemon_id, ctx.author.id))
        else:
            # Ambil pokemon aktif (fitur select akan ditambahkan nanti)
            cursor.execute('SELECT * FROM pokemons WHERE owner_id = ? ORDER BY id DESC LIMIT 1', (ctx.author.id,))
            
        pokemon = cursor.fetchone()
        conn.close()

        if not pokemon:
            return await ctx.send("Pokémon not found!")

        total_iv = (pokemon['hp_iv'] + pokemon['atk_iv'] + pokemon['def_iv'] + 
                    pokemon['sp_atk_iv'] + pokemon['sp_def_iv'] + pokemon['speed_iv'])
        iv_percentage = (total_iv / 186) * 100

        embed = discord.Embed(title=f"Level {pokemon['level']} {pokemon['name']}")
        embed.add_field(name="IVs", value=f"HP: {pokemon['hp_iv']}/31\nAtk: {pokemon['atk_iv']}/31\nDef: {pokemon['def_iv']}/31", inline=True)
        embed.add_field(name="Stats", value=f"Sp.Atk: {pokemon['sp_atk_iv']}/31\nSp.Def: {pokemon['sp_def_iv']}/31\nSpeed: {pokemon['speed_iv']}/31", inline=True)
        embed.set_footer(text=f"Total IV %: {iv_percentage:.2f}%")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Management(bot))
