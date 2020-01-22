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
    
    #Creates the nhl command
    @commands.command(pass_context=True)
    async def nhl(self, ctx):
        
        #Grabs all the games that are playing for the day and stores it in a variable
        gameID = requests.get('https://statsapi.web.nhl.com/api/v1/schedule').text
        gameID = json.loads(gameID)

        #Iterates through all of the json data grabbing only the game ID numbers
        game_ids = []
        game_numbers = []
        for d in gameID["dates"]:
            game_numbers.append(d["games"])
            for g in d["games"]:
                game_ids.append(g["gamePk"])

        #Uses the game ID number to grab the data for each game live
        everything = []
        for i in game_ids:
            url = "https://statsapi.web.nhl.com/api/v1/game/" + str(i) + "/feed/live"
            data = requests.get(url).text

            data = json.loads(data)
            #Gets only the Teams and Scores for the games and appends them to a list
            homeTeam = everything.append(data["gameData"]["teams"]["home"]["teamName"])
            awayTeam = everything.append(data["gameData"]["teams"]["away"]["teamName"])
            homeScore = everything.append(data["liveData"]["linescore"]["teams"]["home"]["goals"])
            awayScore = everything.append(data["liveData"]["linescore"]["teams"]["away"]["goals"])

        #Creates a list of lists by splitting the data every two indexes. The reason for this is
        #There will be two columns in the table so the the data needs to be split in groups of 2
        new_list = [everything[i:i+2] for i in range(0, len(everything), 2)]

        #Creates the table using the tabulate module
        await ctx.send(tabulate(new_list, headers=['Home', 'Away'], colalign=('center', 'right')))

#This setup function is necessary otherwise this program will not be able to interact with the main
#bot file
def setup(bot):
    bot.add_cog(NhlCog(bot))
