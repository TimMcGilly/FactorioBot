import asyncio
import FactorioBot.helper as helper
from discord.ext import commands


class FactorioHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx, command, cooldownUse, val: str):
        if cooldownUse == 'cooldown' or cooldownUse == 'cd':
            cooldownUse = 'cooldown'
        elif cooldownUse == 'use' or cooldownUse == 'u':
            cooldownUse = 'use'
        else:
            await ctx.send("Invalid argument. Valid arguments: `cooldown`, `cd`, `use`, `u`.")
            return

        if val.isdigit():
            parsedVal = int(val)
        else:
            await ctx.send("Invalid argument: value is not an integer.")
            return

        helper.set_config(command, cooldownUse, parsedVal)
        self.bot.unload_extension("cogs.factoriocontrol")
        self.bot.load_extension("cogs.factoriocontrol")


# Setups cog
def setup(bot):
    bot.add_cog(FactorioHelper(bot))
