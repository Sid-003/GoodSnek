from discord.ext import commands

class Info(commands.Cog):
    """Basic info about the bot. Includes ping command and stuff idk"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("ur mum gay")

    @commands.command(name='clean')
    async def ping(self, ctx):
        messages = [x for x in await ctx.channel.history(limit = 100, before=ctx.message).flatten() if x.author.id == ctx.me.id or x.content.startswith('?')]
        await ctx.channel.delete_messages(messages)

def setup(bot):
    bot.add_cog(Info(bot))