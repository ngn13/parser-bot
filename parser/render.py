import nextcord
from parser.utils import *

class Render():
    pass

class CallButtonRender(Render):
    async def init(self, call, inter):
        calll = call.split(">")
        if calll[0] == "msg":
            await self.msg(inter, calll)
        elif calll[0] == "role":
            await self.role(inter, calll)
        else:
            raise Exception("unknown callback function")

    async def msg(inter, calll):
        msgl = calll[1].split(" ")
        for i in range(len(msgl)):
            pass
        await inter.channel.send(listToStr(msgl))

    async def int_msg(inter, calll):
        msgl = calll[1].split(" ")
        for i in range(len(msgl)):
            pass
        await inter.response.send_message(listToStr(msgl))
    
    async def role(inter, calll):
        roleid = calll[1]
        role = nextcord.utils.get(inter.guild.roles, id=int(roleid))
        await inter.user.add_roles(role)

class CallDropdownOptionRender(Render):
    async def init(self, name, call, inter:nextcord.Interaction):
        calll = call.split(">")
        if calll[0] == "msg":
            await self.msg(inter, calll, name)
        elif calll[0] == "role":
            await self.role(inter, calll)
        else:
            raise Exception("unknown callback function")

    async def msg(inter, callol, oname):
        msgl = callol[1].split(" ")
        for i in range(len(msgl)):
            if msgl[i] == "-s":
                msgl[i] = oname
        await inter.channel.send(listToStr(msgl))

    async def int_msg(inter, callol, oname):
        msgl = callol[1].split(" ")
        for i in range(len(msgl)):
            if msgl[i] == "-s":
                msgl[i] = oname
        await inter.response.send_message(listToStr(msgl))
    
    async def role(inter, callol):
        roleid = callol[1]
        role = nextcord.utils.get(inter.guild.roles, id=int(roleid))
        await inter.user.add_roles(role)

class CallDropdownCallbackRender(Render):
    async def init(self, name, call, inter:nextcord.Interaction):
        calll = call.split(">")
        if calll[0] == "msg":
            await self.msg(inter, calll, name)
        elif calll[0] == "role":
            await self.role(inter, calll)
        else:
            raise Exception("unknown callback function")

    async def msg(inter, callol, oname):
        msgl = callol[1].split(" ")
        for i in range(len(msgl)):
            if msgl[i].startswith("-s"):
                try:
                    msgl[i] = oname[int(msgl[i][2])-1]
                except:
                    pass
        await inter.channel.send(listToStr(msgl))

    async def int_msg(inter, callol, oname):
        msgl = callol[1].split(" ")
        for i in range(len(msgl)):
            if msgl[i].startswith("-s"):
                try:
                    msgl[i] = oname[int(msgl[i][2])]
                except:
                    pass
        await inter.response.send_message(listToStr(msgl))
    
    async def role(inter, callol):
        roleid = callol[1]
        role = nextcord.utils.get(inter.guild.roles, id=int(roleid))
        await inter.user.add_roles(role)