import json
import urllib.parse
import discord
from discord.ext import commands
from requests import Response


class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://jisho.org/api/v1/search/words'

    @commands.command(name='lookup')
    async def dict(self, ctx, *, lword: str):
        async with self.bot.session.get(self.url + f'?keyword={lword}') as j:
            try:
                dict = await j.json()
            except:
                return "You messed up boi."

        data = dict["data"]
        word = data[0]
        title = word["slug"]
        senses = word["senses"]
        definitions = []
        for sense in senses:
            definitions.append('; '.join(sense["english_definitions"]))
        kanji = f'https://jisho.org/search/{title}%20%23kanji'

        fdef = [f'{i+1}. {definition}' for i, definition in enumerate(definitions)]

        embed = discord.Embed()
        embed.set_author(name=title, url=f'https://jisho.org/search/{urllib.parse.quote(lword)}')
        embed.description = f'[Kanji Details]({kanji})'
        embed.add_field(name='Reading', value=word["japanese"][0]["reading"])
        embed.add_field(name='Definitions', value='\n'.join(fdef), inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Dictionary(bot))