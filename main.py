;;# =========================
;;
@bot.tree.command(name="start", description="Mulai be;rmain")
async def start(interaction: discord.Interaction):
    user_id = interaction.user.id

    if user_id not in coins:
        coins[user_id] = 1000
        pokemon_db[user_id] = []
        await interaction.response.send_message(
            "Petualangan dimulai! Kamu mendapat 1000 coins."
        )
    else:
        await interaction.response.send_message(
            "Kamu sudah pernah start."
        )

# =========================
# MONEY
# =========================

@bot.tree.command(name="money", description="Cek coins")
async def money(interaction: discord.Interaction):
    user_id = interaction.user.id
    amount = coins.get(user_id, 0)

    await interaction.response.send_message(
        f"Coins kamu: {amount}"
    )

# =========================
# ADMIN GIVE COINS
# =========================

@bot.tree.command(name="givecoins", description="Admin give coins")
async def givecoins(
    interaction: discord.Interaction,
    member: discord.Member,
    amount: int
):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Khusus admin!",
            ephemeral=True
        )
        return

    user_id = member.id

    if user_id not in coins:
        coins[user_id] = 0

    coins[user_id] += amount

    await interaction.response.send_message(
        f"Berhasil memberi {amount} coins ke {member.mention}"
    )

# =========================
# CATCH POKEMON
# =========================

@bot.tree.command(name="catch", description="Tangkap Pokémon random")
async def catch(interaction: discord.Interaction):
    user_id = interaction.user.id

    pokemon = random.choice(pokemon_list)

    if user_id not in pokemon_db:
        pokemon_db[user_id] = []

    pokemon_db[user_id].append(pokemon)

    await interaction.response.send_message(
        f"Kamu menangkap {pokemon}!"
    )

# =========================
# LIST POKEMON
# =========================

@bot.tree.command(name="pokemon", description="Lihat Pokémon")
async def pokemon(interaction: discord.Interaction):
    user_id = interaction.user.id

    pokemons = pokemon_db.get(user_id, [])

    if not pokemons:
        await interaction.response.send_message(
            "Kamu belum punya Pokémon."
        )
        return

    text = "\n".join(pokemons)

    await interaction.response.send_message(
        f"Pokémon kamu:\n{text}"
    )

# =========================
# BATTLE
# =========================

@bot.tree.command(name="battle", description="Battle dengan player")
async def battle(
    interaction: discord.Interaction,
    member: discord.Member
):

    user1 = interaction.user.id
    user2 = member.id

    if user1 == user2:
        await interaction.response.send_message(
            "Tidak bisa melawan diri sendiri."
        )
        return

    power1 = random.randint(1, 100)
    power2 = random.randint(1, 100)

    if power1 > power2:
        winner = interaction.user.mention
        coins[user1] = coins.get(user1, 0) + 200
        result = "mendapat 200 coins"

    elif power2 > power1:
        winner = member.mention
        coins[user2] = coins.get(user2, 0) + 200
        result = "mendapat 200 coins"

    else:
        await interaction.response.send_message(
            "Battle seri!"
        )
        return

    await interaction.response.send_message(
        f"Pemenang battle: {winner}\n{result}"
    )

# =========================
# RESET ECONOMY
# =========================

@bot.tree.command(name="reseteconomy", description="Reset semua economy")
async def reseteconomy(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Khusus admin!",
            ephemeral=True
        )
        return

    coins.clear()
    pokemon_db.clear()

    await interaction.response.send_message(
        "Semua economy berhasil direset!"
    )

# =========================
# DAILY
# =========================

@bot.tree.command(name="daily", description="Claim daily")
async def daily(interaction: discord.Interaction):
    user_id = interaction.user.id

    reward = random.randint(100, 500)

    if user_id not in coins:
        coins[user_id] = 0

    coins[user_id] += reward

    await interaction.response.send_message(
        f"Kamu mendapat {reward} coins!"
    )

# =========================
# HELP COMMAND
# =========================

@bot.tree.command(name="help", description="Lihat semua command")
async def help_command(interaction: discord.Interaction):

    text = (
        "POKEMON BOT COMMANDS

"
        "/start = Mulai bermain
"
        "/money = Lihat coins
"
        "/catch = Tangkap Pokémon
"
        "/pokemon = Lihat Pokémon
"
        "/battle @user = Battle player
"
        "/daily = Claim daily
"
        "/shop = Lihat shop

"
        "ADMIN COMMANDS
"
        "/givecoins @user jumlah
"
        "/reseteconomy"
    )

    await interaction.response.send_message(text)

# =========================
# SHOP
# =========================

@bot.tree.command(name="shop", description="Lihat shop")
async def shop(interaction: discord.Interaction):

    text = (
        "SHOP\n"
        "Pokeball = 100\n"
        "Masterball = 1000\n"
        "Potion = 250"
    )

    await interaction.response.send_message(text)

# =========================
# RUN BOT
# =========================

bot.run(TOKEN)