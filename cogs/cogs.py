from discord.ext import commands

class Cogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group('cogs')
    @commands.is_owner()
    async def cogs(self, ctx):
        pass


    @cogs.command(name='load')
    async def load_cog(self, ctx, name:str):
        try:
            ctx.bot.load_extension(f'cogs.{name}')
            await ctx.message.add_reaction('👍')
        except Exception as e:
            await ctx.send(f'Error while trying to load cog{name}: {e}')

    @cogs.command(name='unload')
    async def unload_cog(self, ctx, name: str):
        try:
            ctx.bot.unload_extension(f'cogs.{name}')
            await ctx.message.add_reaction('👍');
        except Exception as e:
            await ctx.send(f'Error while trying to load cog{name}: {e}')

    @cogs.command(name='reload')
    async def reload_cog(self, ctx, name: str):
        try:
            ctx.bot.reload_extension(f'cogs.{name}')
            await ctx.message.add_reaction('👍');
        except Exception as e:
            await ctx.send(f'Error while trying to load cog{name}: {e}')

def setup(bot):
    bot.add_cog(Cogs(bot))