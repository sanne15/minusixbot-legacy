import discord
from discord import app_commands
from discord.ext import commands
import random
import datetime

from cogs.fetchData import fetchData

class economy(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.db = bot.mongoConnect["discord"]["Economy"]
    
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

  @app_commands.command(name = "work", description = "Let's make money honestly")
  async def work(self, interaction: discord.Interaction):
    
    # Fetch user data
    userData, collection = await fetchData(self.bot, interaction.user.id, "Economy")

    # Check Cooldown
    try:
      if not await check_cooldown(userData, "last_worked"):
        try:
          minutes_left = 60 - ((datetime.datetime.now() - datetime.datetime.strptime(userData["last_worked"], "%Y-%m-%d %H:%M:%S.%f")).seconds // 60)
        except Exception as e:
          print(e)
        await interaction.response.send_message(f"You can work after **{minutes_left}** minutes!")
        return
    except Exception as e:
      print(e)
      
    print("check 2")
    # Generate Random Number
    moneyRecieved = random.randint(100, 500)    
    
    # Update data
    userData["coins"] += moneyRecieved
    userData["last_worked"] = str(datetime.datetime.now())
    
    await collection.replace_one({"_id": interaction.user.id}, userData)
    await interaction.response.send_message(f"You've earned {moneyRecieved} coins, working in the office!")

  @app_commands.command(name = "wallet", description = "check your coins in your wallet")
  async def wallet(self, interaction: discord.Interaction):

    # Fetch user data
    userData, collection = await fetchData(self.bot, interaction.user.id, "Economy")

    await interaction.response.send_message(f"You have {userData['coins']} coins in your wallet.")

  @app_commands.command(name="rank", description="show the leaderboard of your economy")
  async def leaderboard(self, interaction: discord.Interaction):
    collection = self.bot.mongoConnect["discord"]["Economy"]
    try:
        leaderboard = collection.find().sort("coins", -1).limit(10)
    except Exception as e:
        print("Error in leaderboard" + str(e))
    leaderboard_list = []
    try:
        for i, each in enumerate(await leaderboard.to_list(length=10)):
          member_id = each["_id"]
          member = await self.bot.fetch_user(member_id)
          leaderboard_list.append(f"{i+1}: {member.name if member else '[DELETED ACCOUNT]'} - {each['coins']} coins")
    except Exception as e:
        print("Error!!" + str(e))
    leaderboard_embed = discord.Embed(title="Top Economy Rankings",                         description="\n".join(leaderboard_list),                        color=0xFFD700)
    
    await interaction.response.send_message(embed=leaderboard_embed)
  
  @app_commands.command(name="홀짝", description="play the odd-even game")
  @app_commands.choices(guess=[app_commands.Choice(name="even", value="even"), 
                               app_commands.Choice(name="odd", value="odd")])
  async def odd_even_game(self, interaction: discord.Interaction, bet: int, guess: str):
      
    # Fetch user data
    userData, collection = await fetchData(self.bot, interaction.user.id, "Economy")
    
    # Check if user has enough coins for bet
    if bet > userData["coins"]:
      await interaction.response.send_message("도박중독, 무엇을 상상하든 그 이상을 파괴합니다")
      return
    
    # Generate random number between 1 - 1000
    random_num = random.randint(1, 1000)
    
    # Determine if random number is odd or even
    if random_num % 2 == 0:
      result = "even"
    else:
      result = "odd"
    
    # Determine if the user's guess is correct
    if guess == result:
      userData["coins"] += bet
      await interaction.response.send_message(f"{random_num}! Your guess was correct!")
    else:
      userData["coins"] -= bet
      await interaction.response.send_message(f"{random_num}! Your guess was wrong...")
        
    # Update data
      await collection.replace_one({"_id": interaction.user.id}, userData)

async def check_cooldown(userData, column):
  time_now = datetime.datetime.now()
  try:
    last = datetime.datetime.strptime(userData[column], "%Y-%m-%d %H:%M:%S.%f")
  except:
    return True
  print("check 1.25")
  if column == "last_begged":
    if (time_now - last).seconds < 1800:
      return False
    else:
      return True

  if column == "last_worked":
    if (time_now - last).seconds < 3600:
      return False
    else:
      return True


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    economy(bot),
    guilds=[discord.Object(id=567636974979121163)]
  )