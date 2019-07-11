import traceback
import discord
from datetime import  datetime as dt
import sys
from  discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingRequiredArgument, BadArgument, Context

import  config

modules = ['cogs.info', 'cogs.dev', 'cogs.cogs', 'cogs.image']


def _prefix_callback(bot, msg):
    user_id = bot.user.id
    return  [f'<@!{user_id}> ', f'<@{user_id}> ', '?']

class GoodSnek(commands.Bot):
    def __init__(self):
        super().__init__(_prefix_callback, description='very cool bot')
        for cog in modules:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Failed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        print(f'Ready!')


