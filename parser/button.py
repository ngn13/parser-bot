import nextcord
from parser.utils import *
from parser.render import *

class Button(nextcord.ui.Button):
    def __init__(self, msg, color, url, callb):
        self.callb = callb

        if color == "blurple":
            color = nextcord.ButtonStyle.blurple
        elif color == "grey":
            color = nextcord.ButtonStyle.grey
        elif color == "gray":
            color = nextcord.ButtonStyle.gray
        elif color == "green":
            color = nextcord.ButtonStyle.green
        elif color == "red":
            color = nextcord.ButtonStyle.red
        elif color == "url":
            color = nextcord.ButtonStyle.url
        else:
            raise Exception("unknown color for button")

        if url.replace(" ", "") != "NONE":
            super().__init__(label=msg, url=url, style=color)
        else:
            super().__init__(label=msg, style=color)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            if self.callb.replace(" ", "") != "NONE":
                await CallButtonRender.init(CallButtonRender, self.callb, interaction)
        except Exception as e:
            embed = nextcord.Embed(title="Error while interaction", description=str(e), color=0xEE1786)
            await interaction.channel.send(embed=embed)