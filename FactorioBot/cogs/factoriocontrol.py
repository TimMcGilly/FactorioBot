import io
import asyncio
import os

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

    async def enqueue(self, func_name, ctx, *args, **kwargs):
        if 'screenshot' in kwargs:
            screenshot_flag = kwargs['screenshot']
        else:
            screenshot_flag = True
        # Adds the message id, function name, ctx and arguments as a flat list to end of queue
        self.command_queue.append([screenshot_flag, func_name, ctx, *args])

        # Starts executing queue if not already
        if not self.currently_executing:
            await self.execute_command_queue()

    async def execute_command_queue(self):
        # Sets the currently_executing flag so that enqueue doesn't launch multiple of these functions
        self.currently_executing = True

        while self.command_queue:
            # Gets next function and args to execute
            current_command = self.command_queue.pop(0)

            # Calls function which is second index and unpacks the arguments and pass them into the function.
            await current_command[1](*current_command[2:])

            if current_command[0]:
                await self.screenshot(current_command[2])

        self.currently_executing = False

    # Helper functions
    async def screenshot(self, ctx):
        shot = p.screenshot()  # Returns a PIL Image
        imgbytes = io.BytesIO()

        shot.save(imgbytes, format="JPEG")

        imgbytes.seek(0)
        await ctx.send(file=discord.File(fp=imgbytes, filename="file.jpg"))

    @commands.command()
    async def output_command_queue(self, ctx):
        embed = discord.Embed(title="Command Queue",
                              description="Queue of factorio commands to be run.", color=0x00ff00)
        for counter, item in enumerate(self.command_queue):
            # Set name to place in queue and content to the person message with prefix stripped
            embed.add_field(name=str(counter + 1) + ".", value=item[2].message.content.strip(item[2].prefix))

        print(self.command_queue)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(*helper.get_config('walk'))
    async def walk(self, ctx, direction, length: int):

        key = None
        direction = direction.lower()

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
    @commands.cooldown(*helper.get_config('say'))
    async def say(self, ctx, *, message):
        if len(message) < 100:
            await self.enqueue(self.exec_say, ctx, message)

    @commands.command()
    @commands.cooldown(*helper.get_config('craft'))
    async def craft(self, ctx, item, count):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../items.txt')

        if count.isdigit() is False or count < 1:
            await ctx.send("That is a invalid number of items to craft.")
        else:
            with open(filename, "r") as fp:
                recipes = fp.readlines()
            recipes = [x.strip() for x in recipes]

            if item in recipes:
                await self.enqueue(self.exec_craft, ctx, item, count)
            else:
                await ctx.send(
                    "Invalid Argument: Specified recipe name not found.\nPlease check for typos or type `!crafting_help` to get a list of all the items.")

    @commands.command()
    @commands.cooldown(*helper.get_config('research'))
    async def research(self, ctx, tech):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../techs.txt')

        with open(filename, "r") as fp:
            techs = fp.readlines()
        techs = [x.strip() for x in techs]

        if tech in techs:
            await self.enqueue(self.exec_research, ctx, tech)
        else:
            await ctx.send(
                "Invalid Argument: Specified research name not found.\nPlease check for typos or type `!research_help` to get a list of all the techs.")

    @commands.command()
    @commands.cooldown(*helper.get_config('place'))
    async def place(self, ctx, item, direction="N", distance: int = 1, rotation="N"):
        # Item validation
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../items.txt')
        with open(filename, "r") as fp:
            recipes = fp.readlines()
        recipes = [x.strip() for x in recipes]
        if item in recipes:

            # Direction validation
            direction = helper.get_valid_direction(direction)
            if direction is not None:
                rotation = helper.get_valid_direction(direction)
                if rotation is not None:
                    await self.enqueue(self.exec_place, ctx, item, direction, distance, rotation)
                else:
                    await ctx.send("Please enter a valid rotation. Default is N.")
            else:
                await ctx.send("Please enter a valid direction")
        else:
            await ctx.send(
                "Invalid Argument: Specified item name not found.\nPlease check for typos or type `!crafting_help` to get a list of "
                "all the items")

    @commands.command()
    @commands.cooldown(*helper.get_config('place'))
    async def pick_up(self, ctx, direction="N", distance: int = 1):
        # Direction validation
        direction = helper.get_valid_direction(direction)
        if direction is not None:
            await self.enqueue(self.exec_pick_up, ctx, direction, distance)
        else:
            await ctx.send("Please enter a valid direction")

    @commands.command()
    @commands.cooldown(*helper.get_config('view_gui'))
    async def view_inventory(self, ctx):
        await self.enqueue(self.exec_view_inventory, ctx, screenshot=False)

    @commands.command()
    @commands.cooldown(*helper.get_config('view_gui'))
    async def view_tech(self, ctx):
        await self.enqueue(self.exec_view_tech, ctx, screenshot=False)

    '''Executes the commands in factorio'''

    async def exec_walk(self, ctx, direction, key, length):
        await ctx.send("Moving {0} for {1} seconds.".format(direction, length))
        p.keyDown(key)
        await asyncio.sleep(length)
        p.keyUp(key)

    async def exec_say(self, ctx, message):
        p.press("`")
        p.typewrite(message, interval=0)
        p.press("enter")
        await ctx.send("Message sent.")

    async def exec_craft(self, ctx, item, count):
        output = await helper.SendFactorioCommand("craft_item_d", count, item)
        if output.startswith("ERROR"):
            output = "Invalid Command: Requested to craft more than possible or invalid recipe. " \
                     "(please use data.raw recipe names)"
        else:
            output = ("Started crafting {0} {1}(s).").format(output, item)
        await ctx.send(output)

    async def exec_research(self, ctx, tech: str = None):
        if tech is not None:
            output = await helper.SendFactorioCommand("set_research_d", tech)
        else:
            output = await helper.SendFactorioCommand("set_research_d")

        if output.startswith("ERROR"):
            output = "Invalid Command: Invalid technology or unexpected error. " \
                     "(please use data.raw technology names)"
        await ctx.send(output)

    async def exec_place(self, ctx, item, direction, distance, rotation):
        output = await helper.SendFactorioCommand("place_item_d", item, direction, str(distance), rotation)
        if output.startswith("ERROR"):
            await ctx.send("A error occurred.")
        else:
            output = "Successfully placed " + item

        await ctx.send(output)

    async def exec_pick_up(self, ctx, direction, distance):
        output = await helper.SendFactorioCommand("pick_up_item_d", direction, str(distance))
        if output.startswith("ERROR"):
            await ctx.send("A error occurred.")

        await ctx.send(output)

    async def exec_view_inventory(self, ctx):
        p.press("e")
        await self.screenshot(ctx)
        p.press("e")
        await asyncio.sleep(0.5)

    async def exec_view_tech(self, ctx):
        p.press("t")
        await self.screenshot(ctx)
        p.press("t")
        await asyncio.sleep(0.5)


# Setups cog
def setup(bot):
    bot.add_cog(FactorioControl(bot))
