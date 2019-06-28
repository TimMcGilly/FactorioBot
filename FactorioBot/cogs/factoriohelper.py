import os

import discord
from discord.ext import commands
import pyautogui as p
from PIL import Image, ImageFont, ImageDraw, ImageEnhance


class FactorioHelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crafting_help(self, ctx):
        embed = discord.Embed(title="Crafting Help", description="These are all the possible items to craft.\n More "
                                                                 "info at https://stable.wiki.factorio.com/Data.raw. "
                                                                 "Anything under recpie should work. ", color=0x00ff00)
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


# Setups cog
def setup(bot):
    bot.add_cog(FactorioHelper(bot))
