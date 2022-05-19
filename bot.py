import parser
from settings import *

import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions,  CheckFailure, check, MissingPermissions
from nextcord import Interaction

settings = Settings()
prsr = parser.Parser(settings)

client = nextcord.Client()

client = commands.Bot(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print("Bot online")

@client.event
async def on_message(msg):
    if msg.author != client.user:
        result = prsr.parse(str(msg.content))
        if result != False:
            await msg.channel.send(result[1], view=result[0])

client.run(settings.token) 