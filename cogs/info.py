from discord.ext import commands

class Info(commands.Cog):
    """Basic info about the bot. Includes ping command and stuff idk"""

    def __init__(self, bot):
        self.bot = bot
        self.atext = 'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９'
        self.charmap = {}
        al = 97
        ind = 0
        for i in range(len(self.atext)):
            if i == 26:
                al = 65
                ind = 0
            elif i == 52:
                al = 48
                ind = 0
            self.charmap[chr(ind + al)] = self.atext[i]
            ind += 1
        print(self.charmap)



    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("ur mum gay")

    @commands.command(name='clean')
    async def ping(self, ctx):
        messages = [x for x in await ctx.channel.history(limit = 100, before=ctx.message).flatten() if x.author.id == ctx.me.id or x.content.startswith('?')]
        await ctx.channel.delete_messages(messages)

    @commands.command(name='aesthetic')
    async def aesthetic(self, ctx, *, str):
        tosend = ''
        for c in str:
            if c in self.charmap:
                tosend += self.charmap[c]
            else:
                if c == ' ':
                    tosend += ' '
                tosend += c
        await ctx.send(tosend)



def setup(bot):
    bot.add_cog(Info(bot))