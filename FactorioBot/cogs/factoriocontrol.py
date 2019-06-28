import io
import asyncio
from discord.ext import commands
import discord
import FactorioBot.helper as helper
import pyautogui as p

from FactorioBot import config


class FactorioControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_queue = []
        self.currently_executing = False

    '''Queue functions'''

    async def enqueue(self, message_id, func_name, *args):
        # Adds the message id, function name and arguments as a flat list to end of queue
        self.command_queue.append([message_id, func_name, *args])

        # Starts executing queue if not already
        if not self.currently_executing:
            await self.execute_command_queue()

    async def execute_command_queue(self):
        # Sets the currently_executing flag so that enqueue doesn't launch multiple of these functions
        self.currently_executing = True

        while self.command_queue:
            # Gets next function and args to execute
            current_command = self.command_queue.pop()

            # Calls function which is first index and unpacks the arguments and pass them into the function.
            await current_command[0](*current_command[1:])

            await self.screenshot(current_command[1])
        self.currently_executing = False

    # Helper functions
    async def screenshot(self, ctx):
        shot = p.screenshot()  # Returns a PIL Image
        imgbytes = io.BytesIO()

        shot.save(imgbytes, format="JPEG")

        imgbytes.seek(0)
        await ctx.send(file=discord.File(fp=imgbytes, filename="file.jpg"))

    @commands.command()
    async def walk(self, ctx, direction, length: int):

        key = None

        if direction == "north" or direction == "n":
            key = "w"
        elif direction == "south" or direction == "s":
            key = "s"
        elif direction == "west" or direction == "w":
            key = "a"
        elif direction == "east" or direction == "e":
            key = "d"

        if key is not None and 0 < length < 11:
            await self.enqueue(self.exec_walk, ctx, direction, key, length)

        else:
            await ctx.send("Invalid direction or length limit reached.")

    @commands.command()
    async def sayInGame(self, ctx, *, message):
        if len(message) < 100:
            await self.enqueue(self.exec_sayInGame, ctx, message)

    # Test command
    @commands.command()
    async def long_command(self, ctx):
        print("long command")
        await self.enqueue(self.exec_long_command, ctx, "dave")

    @commands.command()
    async def mod_output_test(self, ctx, *, message):
        await self.enqueue(self.exec_mod_output_test, ctx, message)

    @commands.command()
    async def craft_item(self, ctx, item, count):
        await self.enqueue(self.exec_craft_item, ctx, item, count)

    '''Executes the commands in factorio'''

    async def exec_walk(self, ctx, direction, key, length):
        await ctx.send("Moving {0} for {1} seconds.".format(direction, length))
        p.keyDown(key)
        await asyncio.sleep(length)
        p.keyUp(key)

    async def exec_sayInGame(self, ctx, message):
        p.press("`")
        p.typewrite(message, interval=0)
        p.press("enter")
        await ctx.send("Message sent.")

    async def exec_craft_item(self, ctx, item, count):
        output = await helper.SendFactorioCommand("craft_item_d", count, item)
        if output.startswith("ERROR"):
            output = "Invalid Command: Requested to craft more than possible or invalid recipe."
        await ctx.send(output)
    # Test exec
    async def exec_long_command(self, ctx, bob):
        await asyncio.sleep(2)
        await ctx.send(bob)

    async def exec_mod_output_test(self, ctx, message):
        output = await helper.SendFactorioCommand('write_test_d', message)
        await ctx.send(output)




# Setups cog
def setup(bot):
    bot.add_cog(FactorioControl(bot))
