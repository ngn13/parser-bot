import nextcord

class DiscordView(nextcord.ui.View):
    def __init__(self, items):
        super().__init__()
        for item in items:
            if item != None:
                self.add_item(item)