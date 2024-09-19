import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice

class fruit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
      
    @app_commands.command(
      name = "fruits",
      description = "Get a random fruity fruits"
    )

    @app_commands.describe(
      fruit = "The fruit you want to get",
      ratings = "The ratings you want to rate")

    @app_commands.choices(
      ratings = [
        Choice(name = "one", value = 1),
        Choice(name = "two", value = 2),
        Choice(name = "three", value = 3),
        Choice(name = "four", value = 4),
        Choice(name = "five", value = 5),
      ]
    )
  
    async def fruits(
      self,
      interaction: discord.Interaction,
      fruit: str,
      ratings : int) -> None:

      await interaction.response.send_message(f"{fruit} is {ratings} stars")

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(
    fruit(bot),
    guilds=[discord.Object(id=567636974979121163)]
  )