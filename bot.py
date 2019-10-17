import sys
import traceback

import aiohttp
from darkflow.net.build import TFNet
from  discord.ext import commands

modules = ['cogs.info', 'cogs.dev', 'cogs.cogs', 'cogs.image', 'cogs.dictionary']


def _prefix_callback(bot, msg):
    user_id = bot.user.id
    return  [f'<@!{user_id}> ', f'<@{user_id}> ', '?']

class GoodSnek(commands.Bot):
    def __init__(self):
        super().__init__(_prefix_callback, description='very cool bot')
        options = {"pbLoad": "modeldata/model.pb", "metaLoad": "modeldata/config.meta", "threshold": 0.1}
        self.tfnet = TFNet(options)
        self.session = aiohttp.ClientSession(loop=self.loop)
        for cog in modules:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Failed to load extension {cog}.', file=sys.stderr)
                traceback.print_exc()

    async def on_ready(self):
        print(f'Ready!')


