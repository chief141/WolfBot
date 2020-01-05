 #!/usr/bin/python3

import discord
import os
from discord.ext import commands, tasks
from collections import defaultdict
from discord.utils import get

from wolframclient.evaluation import WolframLanguageSession, WolframLanguageAsyncSession
from wolframclient.language import wl, wlexpr
from wolframclient.evaluation import SecuredAuthenticationKey, WolframCloudSession
from wolframclient.exception import WolframEvaluationException, WolframLanguageException, WolframKernelException
from PIL import Image

# Define paths
#img_path = 'D:/dev/discordbots/WolfBot/output/output.jpg'
img_path = '/home/pi/WolfBot/output/output.jpg'
#kernel_path = 'D:/Program Files/Wolfram Research/Wolfram Engine/12.0/WolframKernel.exe'
kernel_path = '/opt/Wolfram/WolframEngine/12.0/Executables/WolframKernel'

# Authentication Key
sak = SecuredAuthenticationKey(

    't9JwbVPeUiX0G38n8/GtrLcz0S1vXrTiNfvHbNFl5U0=',

    'dbbLmj8rDSrTEe0A+baPcMIFgFhmVPfFMdLg4trDuFc=')
#

# Enlarges image output from Wolfram calculation, and then saves as png #
def enlarge():
    img = Image.open(img_path, 'r')
    img_w, img_h = img.size

    background = Image.new('RGB', (img_w + 25, img_h + 25), (255, 255, 255, 255))
    bg_w, bg_h = background.size
    background.paste(img,(13,12))
    background.save(img_path)

# Creates a discord.Embed object #
def createEmbed(t):
    # Embed message
    embed = discord.Embed(
        title = t)
    return embed

client = commands.Bot(command_prefix = '$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
@commands.has_any_role('Admin', 'Bot Henchmen', 'Development Team')
async def session(ctx):

    async with ctx.typing():
        channel = ctx.message.channel
        def check(m):
            return m.channel == channel and (m.content).startswith('WL ') and m.author == ctx.message.author

    async with WolframLanguageAsyncSession(kernel_path) as session:

        async with ctx.typing():
            # Start Asynchronous Wolfram Kernel thread #
            await session.start()
            # Tell user that the session has successfully started
            start_alert = discord.Embed(
                title = f'**Wolfram Session Started!**',
                color = discord.Color.blue(),
                description = f'Initiated by\n{ctx.message.author.mention}')
            await ctx.send(embed = start_alert)

        # Prepares the user input to be passed into Wolfram functions that export the output image, and limit the time of the computation 
        begin = f'Export["{img_path}", TimeConstrained['
        end = ', 60, "Your computation has exceeded one minute."]]'

        # Wait for discord user to enter input, and save message to msg.
        msg = await client.wait_for('message', check = check)

        # save string from message object to a string variable
        wolfcommand = msg.content 
        wolfcommand = wolfcommand.replace('WL ', '')

        # concatenate the full command for passing to Wolfram
        export = begin + wolfcommand + end 


        # Loop session, sending output from initial input, taking in new input, repeat.
        while msg.content != 'WL exit' :
            if msg.content != 'WL exit':
                try:
                    async with ctx.typing():
                        await session.evaluate(wlexpr(export))
                        enlarge()
                        
                        # Send image from Wolfram calculation results
                        await ctx.send(file=discord.File(img_path))
                    
                    # Wait for new input from user
                    msg = await client.wait_for('message', check = check)
                    wolfcommand = msg.content
                    wolfcommand = wolfcommand.replace('WL ', '')
                    export = begin + wolfcommand + end
                except WolframLanguageException as err:
                    error = err
                    await ctx.send(error)

        # Loop seninent value detected, closes connection to wolfram kernel
        await session.stop()

    # Send Embed message for end of session #
    end_message = discord.Embed(
        title = f'**Wolfram session terminated!**',
        color = discord.Color.blue(),
        description = f'Session started by\n{ctx.message.author.mention}')
    await ctx.send(embed = end_message)



client.run('NjUzODA3MTM3NjkyMTg4Njcy.Xe8Xlg.-EDzSXrTejAAuJ2sCI-0mfwUxjY')


