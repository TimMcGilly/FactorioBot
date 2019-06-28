import asyncio
import FactorioBot.helper as helper
import os
import discord

from discord.ext import commands
import pyautogui as p
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


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

    @commands.command()
    async def crafting_help(self, ctx):
        embed = discord.Embed(title="Crafting Help", description="These are all the possible items to craft.\n More "
                                                                 "info at https://stable.wiki.factorio.com/Data.raw. "
                                                                 "Anything under recipe should work. ", color=0x00ff00)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../items.txt')
        with open(filename, "r") as fp:
            buffer = 0
            stringBuilder = ""
            count = 1
            for line in fp:
                if (buffer + len(line)) > 1024:
                    embed.add_field(name="Recipes part " + str(count), value=stringBuilder, inline=False)
                    stringBuilder = line
                    buffer = len(stringBuilder)
                    count += 1
                else:
                    buffer += len(line)
                    stringBuilder += line
            embed.add_field(name="Recipes part " + str(count), value=stringBuilder, inline=False)

        await ctx.author.send(embed=embed)

    @commands.command()
    async def research_help(self, ctx):
        embed = discord.Embed(title="Research Help", description="These are all the possible techs to research.\n More "
                                                                 "info at https://stable.wiki.factorio.com/Data.raw. "
                                                                 "Anything under `technology` should work. ",
                              color=0x00ff00)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../techs.txt')
        with open(filename, "r") as fp:
            buffer = 0
            stringBuilder = ""
            count = 1
            for line in fp:
                if (buffer + len(line)) > 1024:
                    embed.add_field(name="Techs part " + str(count), value=stringBuilder, inline=False)
                    stringBuilder = line
                    buffer = len(stringBuilder)
                    count += 1
                else:
                    buffer += len(line)
                    stringBuilder += line
            embed.add_field(name="Techs part " + str(count), value=stringBuilder, inline=False)

        await ctx.author.send(embed=embed)


# Setups cog
def setup(bot):
    bot.add_cog(FactorioHelper(bot))
