import inspect
import textwrap

from discord.ext import  commands
import asyncio

class Dev(commands.Cog):
    """Owner only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        code = code[5:-3]
        async_body = f'async def _func():\n{textwrap.indent(code, " ")}'
        variables = {
            'bot': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author
        }
        variables.update(globals())
        try:
            r = exec(async_body.format(code), variables, locals())

            func = locals()['_func']

            r = await func()

            if r is not None:
                await ctx.send(r)

        except Exception as e:
            await ctx.send(f'Found exception during evaluation: {e}')

def setup(bot):
    bot.add_cog(Dev(bot))