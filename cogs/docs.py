import discord
import os
from discord.ext import commands, tasks
from collections import defaultdict
from discord.utils import get

import embeds

class Docs(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def docs(self, ctx, query = 'none'):
        async with ctx.typing():
            if query == 'none':
                await ctx.send('Please enter a search term, using the syntax `\docs <search term>` (e.g. `\docs Plot`, `\docs integration`).')
            else:
                if query.lower() in ['plot', 'integrate', 'plot3d']:
                    link = f'https://reference.wolfram.com/language/ref/{query.capitalize()}.html'
                else:
                    link = f'https://reference.wolfram.com/search/?q={query}'
                embed = discord.Embed(
                    title = f'Online Wolfram Documentation: \'{query}\'',
                    color = discord.Color.dark_teal(),
                    url = link
                )
                embed.set_footer(text = f'requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed = embed)
    @commands.command()
    async def license(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title = 'Click to see Wolfram\'s license and conditions which we operate under.',
                url = 'https://github.com/trevortrusty/WolfBot/blob/master/LICENSE',
                description = 'MIT License\nCopyright (c) 2018 Wolfram Research Inc.'
            )
            embed.set_footer(text='Wolfram Client Library for Python')
            await ctx.send(embed = embed)
        #https://github.com/trevortrusty/WolfBot/blob/master/LICENSE

def setup(client):
    client.add_cog(Docs(client))