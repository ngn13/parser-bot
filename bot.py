from parser.parser import Parser
from settings import *

import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions,  CheckFailure, check, MissingPermissions
from nextcord import Interaction

settings = Settings()
prsr = Parser(settings)

client = nextcord.Client()

client = commands.Bot(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        try:
            result = prsr.parse(str(msg.content))
        except Exception as e:
                embed = nextcord.Embed(title="Error while parsing", description=str(e), color=0xEE1717)
                return await msg.channel.send(embed=embed)

        if result != False:
            try:
                await msg.channel.send(result[1], view=result[0])
                await msg.delete()
            except Exception as e:
                embed = nextcord.Embed(title="Error while rendering", description=str(e), color=0x17A3EE)
                await msg.channel.send(embed=embed)
            
client.run(settings.token) 