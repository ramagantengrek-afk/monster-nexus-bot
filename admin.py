import discord
from discord.ext import commands
from ..utils.database import get_db_connection
from ..utils.pokeapi import get_pokemon_data, calculate_iv

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Helper untuk mengecek apakah user adalah admin (misal owner bot)
    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(name="givecoin")
    async def give_coin(self, ctx, user: discord.Member, amount: int):
        """Menambahkan saldo ke user tertentu."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user.id,))
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user.id))
        
        conn.commit()
        conn.close()
        await ctx.send(f"Successfully gave **{amount} coins** to {user.mention}!")

    @commands.command(name="givepokemon")
    async def give_pokemon(self, ctx, user: discord.Member, pokemon_name: str, level: int = 1):
        """Memberikan Pokemon spesifik ke user tertentu."""
        pokemon_data = await get_pokemon_data(pokemon_name.lower())
        if not pokemon_data:
            return await ctx.send("Pokemon not found!")

        conn = get_db_connection()
        cursor = conn.cursor()
        
        ivs = calculate_iv()
        cursor.execute('''
        INSERT INTO pokemons (owner_id, species_id, name, level, hp_iv, atk_iv, def_iv, sp_atk_iv, sp_def_iv, speed_iv)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.id, pokemon_data['id'], pokemon_data['name'].capitalize(), level,
              ivs['hp'], ivs['atk'], ivs['def'], ivs['sp_atk'], ivs['sp_def'], ivs['speed']))
        
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user.id,))
        
        conn.commit()
        conn.close()
        await ctx.send(f"Successfully gave a **Level {level} {pokemon_data['name'].capitalize()}** to {user.mention}!")

    @commands.command(name="forcespawn")
    async def force_spawn(self, ctx, pokemon_name: str = None):
        """Memaksa Pokemon muncul di channel saat ini."""
        spawn_cog = self.bot.get_cog('Spawn')
        if not spawn_cog:
            return await ctx.send("Spawn system not loaded!")

        if pokemon_name:
            pokemon = await get_pokemon_data(pokemon_name.lower())
        else:
            from ..utils.pokeapi import get_random_pokemon
            pokemon = await get_random_pokemon()

        if not pokemon:
            return await ctx.send("Pokemon not found!")

        spawn_cog.current_spawns[ctx.channel.id] = pokemon
        
        embed = discord.Embed(title="A wild Pokémon has appeared! (Admin Force)", description="Guess the Pokémon and type `p!catch <name>` to catch it!")
        embed.set_image(url=pokemon['sprites']['front_default'])
        await ctx.send(embed=embed)

    @commands.command(name="setbalance")
    async def set_balance(self, ctx, user: discord.Member, amount: int):
        """Mengatur saldo user ke jumlah tertentu."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user.id,))
        cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (amount, user.id))
        
        conn.commit()
        conn.close()
        await ctx.send(f"Successfully set {user.mention}'s balance to **{amount} coins**.")

    @commands.errorhandler
    async def admin_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("❌ You do not have permission to use this command. Only the bot owner can use admin commands.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
