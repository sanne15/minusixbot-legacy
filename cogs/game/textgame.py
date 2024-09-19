import discord
from discord import app_commands
from discord.ext import commands
import random
import datetime

from cogs.fetchData import fetchData

class game(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.db = bot.mongoConnect["discord"]["TextGame"]
    
  @app_commands.command(name = "beg", description = "beg for money")
  async def beg(self, interaction: discord.Interaction):
    
    # Fetch user data
    userData, collection = await fetchData(self.bot, interaction.user.id, "Economy")
    
    # Check Cooldown
    try:
      if not await check_cooldown(userData, "last_begged"):
        try:
          minutes_left = 30 - ((datetime.datetime.now() - datetime.datetime.strptime(userData["last_begged"], "%Y-%m-%d %H:%M:%S.%f")).seconds // 60)
        except Exception as e:
          print(e)
        await interaction.response.send_message(f"You can beg after **{minutes_left}** minutes!")
        return
    except Exception as e:
      print(e)
    
    # Generate Random Number
    moneyRecieved = random.randint(0, 100)    
    
    # Update data
    userData["coins"] += moneyRecieved
    userData["last_begged"] = str(datetime.datetime.now())
    
    await collection.replace_one({"_id": interaction.user.id}, userData)
    await interaction.response.send_message(f"You've earned {moneyRecieved} coins!")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    economy(bot),
    guilds=[discord.Object(id=567636974979121163)]
  )