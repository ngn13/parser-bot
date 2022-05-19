import nextcord
import ast 

def listToStr(s):
        str1 = "" 
        for ele in s: 
            str1 += ele+" "  
        return str1

def listToStrln(s):
        str1 = "" 
        for ele in s: 
            str1 += ele+"\n"  
        return str1

class CalloRender():
    async def init(self, name, callo, inter:nextcord.Interaction):
        callol = callo.split(">")
        if callol[0] == "msg":
            await self.msg(inter, callol, name)
        elif callol[0] == "role":
            await self.role(inter, callol)
    
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

class CallbRender():
    async def init(self, name, callo, inter:nextcord.Interaction):
        callol = callo.split(">")
        if callol[0] == "msg":
            await self.msg(inter, callol, name)
        elif callol[0] == "role":
            await self.role(inter, callol)
    
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

class Dropdown(nextcord.ui.Select):
    def __init__(self, minv, maxv, plh, options, callb):
        selectOptions = []
        self.optionslist = options
        self.callb = callb
        for option in options:
            if len(option) == 3:
                selectOptions.append(nextcord.SelectOption(label=option[0], description=option[1]))
            elif len(option) == 2:
                selectOptions.append(nextcord.SelectOption(label=option[0]))

        super().__init__(placeholder=plh, min_values=minv, max_values=maxv, options=selectOptions)

    async def callback(self, interaction: nextcord.Interaction):
        for name in self.values:
            for option in self.optionslist:
                if name == option[0]:
                    callo = option[len(option)-1]
                    if callo != "NONE":
                        await CalloRender.init(CalloRender, name, callo, interaction)
        if self.callb != "NONE":
            await CallbRender.init(CallbRender, self.values, self.callb, interaction)

class DiscordView(nextcord.ui.View):
    def __init__(self, items):
        super().__init__()
        for item in items:
            if item != None:
                self.add_item(item)

class Parser:
    def __init__(self, settings):
        self.settings = settings

    def parse_render(self,rlist):
        rlist = rlist.split(":")
        if rlist[0] == "dropdown":
            if len(rlist) != 6:
                raise Exception("illegal argument count for dropdown menu")
            try:
                minv = int(rlist[1])
                maxv = int(rlist[2])
                plh = rlist[3]
                options = ast.literal_eval(rlist[4])
                callb = rlist[5]
            except:
                raise Exception("illegal argument for dropdown menu")

            dropdown_menu = Dropdown(minv, maxv, plh, options, callb)
            return dropdown_menu


    def parse_tokens(self,text):
        tlist = text.split(" ")
        indx_start = 0
        indx_end = 0
        indx_start_old = indx_start
        read_bool = True
        item_list = []
        for i in range(len(tlist)):
            t = tlist[i]
            if t == self.settings.pointer[0]:
                indx_start = i
            elif t == self.settings.pointer[1]:
                if indx_start != indx_start_old:
                    indx_end = i
                    read_bool = False

            if not read_bool:
                rlist = []
                for i in range(indx_start+1, indx_end):
                    rlist.append(tlist[i])
                item_list.append(self.parse_render(listToStr(rlist)))
                indx_start_old = indx_start
                read_bool = True
        
        remove_el_list = text.split(self.settings.remove_pointer)
        for el in remove_el_list:
            if el.startswith(" "+self.settings.pointer[0]) and el.endswith(self.settings.pointer[1]+" "):
                remove_el_list.remove(el)

        return [DiscordView(item_list),listToStr(remove_el_list)]

    def parse(self, text):
        lnlist = text.split("\n")
        if self.settings.cmd == lnlist[0]:
            lnlist.remove(self.settings.cmd)
            return self.parse_tokens(listToStrln(lnlist))
        else:
            return False