import nextcord
from parser.utils import *
from parser.render import *

class Dropdown(nextcord.ui.Select):
    def __init__(self, minv, maxv, plh, options, callb):
        selectOptions = []
        self.optionslist = options
        self.callb = callb

        if len(options) == 0:
            raise Exception("dropdown needs at least one option")

        if plh == "NONE":
            raise Exception("placeholder cant be NONE for dropdown")

        for option in options:
            if len(option) == 3:
                selectOptions.append(nextcord.SelectOption(label=option[0], description=option[1]))
            elif len(option) == 2:
                selectOptions.append(nextcord.SelectOption(label=option[0]))
            else:
                raise Exception("illegal option for dropdown")

        super().__init__(placeholder=plh, min_values=minv, max_values=maxv, options=selectOptions)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            for name in self.values:
                for option in self.optionslist:
                    if name == option[0]:
                        callo = option[len(option)-1]
                        if callo.replace(" ", "") != "NONE":
                            await CallDropdownOptionRender.init(CallDropdownOptionRender, name, callo, interaction)
            if self.callb.replace(" ", "") != "NONE":
                await CallDropdownCallbackRender.init(CallDropdownCallbackRender, self.values, self.callb, interaction)
        except Exception as e:
            embed = nextcord.Embed(title="Error while interaction", description=str(e), color=0xEE1786)
            await interaction.channel.send(embed=embed)