import ast
from parser.dropdown import *
from parser.view import *
from parser.utils import *
from parser.button import *
import nextcord

class Parser:
    def __init__(self, settings):
        self.settings = settings

    def parse_render(self,rlist):
        rlist = rlist.split(self.settings.option_pointer)
        if rlist[0] == "dropdown":
            if len(rlist) != 6:
                raise Exception("illegal argument count for dropdown")
            try:
                minv = int(rlist[1])
                maxv = int(rlist[2])
                plh = rlist[3]
                options = ast.literal_eval(rlist[4])
                callb = rlist[5]
            except:
                raise Exception("illegal argument for dropdown")

            dropdown_menu = Dropdown(minv, maxv, plh, options, callb)
            return dropdown_menu
        elif rlist[0] == "button":
            if len(rlist) != 5:
                raise Exception("illegal argument count for button")
            try:
                msg = rlist[1]
                color = rlist[2]
                url = rlist[3]
                callb = rlist[4]

                button = Button(msg, color, url, callb)
                return button
            except:
                raise Exception("illegal argument for button")


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