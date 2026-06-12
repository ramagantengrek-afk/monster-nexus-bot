import discord
from discord.ext import commands
import random
from ..utils.pokeapi import get_random_pokemon, calculate_iv
from ..utils.database import get_db_connection

class Spawn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_spawns = {} # {channel_id: pokemon_data}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Probabilitas spawn (misal 10%)
        if random.random() < 0.10:
            pokemon = await get_random_pokemon()
            if pokemon:
                self.current_spawns[message.channel.id] = pokemon
                
                embed = discord.Embed(title="A wild Pokémon has appeared!", description="Guess the Pokémon and type `p!catch <name>` to catch it!")
                embed.set_image(url=pokemon['sprites']['front_default'])
                await message.channel.send(embed=embed)

    @commands.command()
    async def catch(self, ctx, name: str):
        pokemon = self.current_spawns.get(ctx.channel.id)
        
        if not pokemon:
            return await ctx.send("There is no wild Pokémon here!")
            
        if name.lower() == pokemon['name'].lower():
            # Simpan ke database
            conn = get_db_connection()
            cursor = conn.cursor()
            
            ivs = calculate_iv()
            cursor.execute('''
            INSERT INTO pokemons (owner_id, species_id, name, hp_iv, atk_iv, def_iv, sp_atk_iv, sp_def_iv, speed_iv)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ctx.author.id, pokemon['id'], pokemon['name'].capitalize(), 
                  ivs['hp'], ivs['atk'], ivs['def'], ivs['sp_atk'], ivs['sp_def'], ivs['speed']))
            
            # Update user if not exists
            cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (ctx.author.id,))
            
            conn.commit()
            conn.close()
            
            del self.current_spawns[ctx.channel.id]
            await ctx.send(f"Congratulations {ctx.author.mention}! You caught a **Level 1 {pokemon['name'].capitalize()}**!")
        else:
            await ctx.send("Wrong name! Try again.")

async def setup(bot):
    await bot.add_cog(Spawn(bot))
