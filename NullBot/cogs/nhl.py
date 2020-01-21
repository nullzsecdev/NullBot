#!/usr/bin/env python3

import json 
import discord
import requests
from tabulate import tabulate
from discord.ext import commands
#Game data found here
# https://statsapi.web.nhl.com/api/v1/game/{game id}/feed/live

class NhlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def nhl(self, ctx):

        gameID = requests.get('https://statsapi.web.nhl.com/api/v1/schedule').text
        gameID = json.loads(gameID)

        game_ids = []
        game_numbers = []
        for d in gameID["dates"]:
            game_numbers.append(d["games"])
            for g in d["games"]:
                game_ids.append(g["gamePk"])

        everything = []
        for i in game_ids:
            url = "https://statsapi.web.nhl.com/api/v1/game/" + str(i) + "/feed/live"
            data = requests.get(url).text

            data = json.loads(data)
    
            homeTeam = everything.append(data["gameData"]["teams"]["home"]["teamName"])
            awayTeam = everything.append(data["gameData"]["teams"]["away"]["teamName"])
            homeScore = everything.append(data["liveData"]["linescore"]["teams"]["home"]["goals"])
            #awayTeam = everything.append(data["gameData"]["teams"]["away"]["teamName"])
            awayScore = everything.append(data["liveData"]["linescore"]["teams"]["away"]["goals"])

        
        new_list = [everything[i:i+2] for i in range(0, len(everything), 2)]
        await ctx.send(tabulate(new_list, headers=['Home', 'Away'], colalign=('center', 'right')))

def setup(bot):
    bot.add_cog(NhlCog(bot))
