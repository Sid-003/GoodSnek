from discord.ext import commands

class Info(commands.Cog):
    """Basic info about the bot. Includes ping command and stuff idk"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("ur mum gay")

def setup(bot):
    bot.add_cog(Info(bot))