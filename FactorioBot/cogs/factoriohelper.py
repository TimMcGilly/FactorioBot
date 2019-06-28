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
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, command: str, cooldownUse, val: str):

        if cooldownUse == 'cooldown' or cooldownUse == 'cd':
            cooldownUse = 'cooldown'
            outputNoun = 'seconds'
        elif cooldownUse == 'use' or cooldownUse == 'u' or cooldownUse == 'uses':
            cooldownUse = 'uses'
            outputNoun = 'times'
        else:
            await ctx.send("Invalid argument. Valid arguments: `cooldown`, `cd`, `uses`, `u`.")
            return

        if val.isdigit():
            parsedVal = int(val)
        else:
            await ctx.send("Invalid argument: value is not an integer.")
            return

        helper.set_config(command, cooldownUse, parsedVal)
        self.bot.unload_extension("cogs.factoriocontrol")
        self.bot.load_extension("cogs.factoriocontrol")
        await ctx.send(command.capitalize() + " " + cooldownUse + " is now set to " + str(parsedVal) + " "
                       + outputNoun + ".")

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

    @commands.command()
    async def help(self, ctx):
        author = ctx.author

        embed = discord.Embed(
            colour=discord.Colour.blurple()
        )
        embed.set_author(
            name='Help',
            icon_url=
            "https://cdn.discordapp.com/attachments/407617128112324629/594297916743614474/factorio_bot_blurple_logo.png")
        embed.add_field(name="!help", value="Returns this help message")
        embed.add_field(name="!walk <direction> <length>",
                        value="Moves the character in a given `<direction>` for a `<length>` number of seconds.\n"
                              "Accepted values for direction are: `n`, `e`, `w`, `s` or `north`, `east`, `west`, `south`. ")
        embed.add_field(name="!say <message>",
                        value="Says the given `<message>` in the factorio chat. Useful for multiplayer.")
        embed.add_field(name="!place <item> <direction> <distance> <rotation>",
                        value="Places an `<item>` from the inventory on the factorio grid.\n"
                              "Adjust the position of the object relative to the player, by specifying"
                              " the `<distance>` away from player in a `<direction>`. \n"
                              "Adjust the `<rotation>` of the object by specifying which side the object has to face. \n"
                              "Accepted values for `<rotation>` and `<direction>` are: "
                              "`n`, `e`, `w`, `s` or `north`, `east`, `west`, `south`. ")
        embed.add_field(name="!pick_up <direction> <distance>",
                        value="Picks up a item from the factorio grid.\n"
                              "Adjust the position of the item to pick up relative to the player, by specifying the "
                              "`<distance>` away from player in a `<direction>`.\n"
                              "Accepted values for `<direction>` are: \n"
                              "`n`, `e`, `w`, `s` or `north`, `east`, `west`, `south`. "
                        )
        embed.add_field(name="!craft <item-to-craft> <count>",
                        value="Crafts the `<count>` of `<item-to-craft>`.\n"
                              "Accepted values for `<item-to-craft>` are:\n"
                              "An item name with spaces replaced with `-` should work. `!crafting_help` will dm you a "
                              "list of all possible recipes."
                        )
        embed.add_field(name="!view_inventory",
                        value="Sends a screenshot of character inventory."
                        )
        embed.add_field(name="!view_tech",
                        value="Sends a screenshot of the current tech tree."
                              
                        )
        embed.add_field(name="!research [tech]", 
                        value="Sets current research to a specified `[tech]`.\n"
                              "Accepted values for `[tech]` are:"
                              "A technology name with spaces replaced with `-` should work. `!reseach_help` will dm you a "
                              "list of all possible technologies.\n"
                              "`!research stop` will stop current research.\n"
                              "Leaving `[tech]` **blank** will be interpreted the same as `!research stop`"
                        )
        embed.add_field(name="!config <command> <cooldownUse> <value>",
                        value="Changes the cooldown configuration values in `config.json`\n"
                              "Sets a `'cooldown'` or `'use'` `value` for a given `<command>`.\n"
                              "Uses are the amount of times a command can be used before a cooldown is triggered.\n"
                              "Cooldown is duration in seconds in which the command cannot be executed by a user.\n"
                              "Accepted values for `<cooldownUse>` are:\n"
                              "`cooldown`, `use`, `uses` or `cd`, `u`."
                        )
       

        await ctx.author.send(embed=embed)


# Setups cog
def setup(bot):
    bot.add_cog(FactorioHelper(bot))
