import asyncio
import pyautogui as p
from discord.ext import commands



class Factorio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def center(self, ctx):
        screenWidth, screenHeight = p.size()

        p.moveTo(screenWidth / 2, screenHeight / 2)

        await ctx.send("did it")

    @commands.command()
    async def walk(self, ctx, direction, length : int):

        key = None

        if direction == "north" or direction == "n":
            key = "w"
        elif direction == "south" or direction == "s":
            key = "s"
        elif direction == "west" or direction == "w":
            key = "a"
        elif direction == "east" or direction == "e":
            key = "d"

        if key is not None and 0<length<11:

            await ctx.send("Moving {0} for {1} seconds.".format(direction, length))
            p.keyDown(key)
            await asyncio.sleep(length)
            p.keyUp(key)


        else:
            await ctx.send("Invalid direction or length limit reached.")

    @commands.command()
    async def sayInGame(self, ctx, *, message):

        if len(message) < 100:
            p.press("`")
            p.typewrite(message, interval=0)
            p.press("enter")
            await ctx.send("Message sent.")

# Setups cog
def setup(bot):
    bot.add_cog(Factorio(bot))