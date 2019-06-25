import asyncio
from discord.ext import commands

class FactorioHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



# Setups cog
def setup(bot):
    bot.add_cog(FactorioHelper(bot))