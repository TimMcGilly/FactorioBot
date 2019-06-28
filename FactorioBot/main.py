import asyncio
import FactorioBot.helper as helper
from discord.ext import commands
import logging
import FactorioBot.config as config

logger = logging.getLogger('discord')

# sets up discord.py logging in chat
logging.basicConfig(level=logging.INFO)

# sets up logging to file
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, description="Bob is your uncle")

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def get_prefix(self, message):
        return "!"

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        await self.process_commands(message)

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, commands.NoPrivateMessage):
            await ctx.send("\N{WARNING SIGN} Sorry, you can't use this command in a private message!")

        elif isinstance(exception, commands.CommandNotFound):
            await ctx.send("\N{WARNING SIGN} That command doesn't exist!")

        elif isinstance(exception, commands.DisabledCommand):
            await ctx.send("\N{WARNING SIGN} Sorry, this command is disabled!")

        elif isinstance(exception, commands.MissingPermissions):
            await ctx.send(f"\N{WARNING SIGN} You do not have permissions to use this command.")

        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention} slow down! Try that again in {exception.retry_after:.1f} seconds")

        elif isinstance(exception, commands.MissingRequiredArgument) or isinstance(exception, commands.BadArgument):
            await ctx.send(f"\N{WARNING SIGN} {exception}")

        elif isinstance(exception, commands.CommandInvokeError):
            raise exception

    async def load_cogs(self, names):
        for name in names:
            self.load_extension(name)


async def run():
    helper.setup_config()
    bot = Bot()
    bot.remove_command('help')

    await bot.load_cogs(["cogs.factoriocontrol", "cogs.factoriohelper"])

    try:
        await bot.start(config.token)
    except KeyboardInterrupt:
        await bot.logout()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
