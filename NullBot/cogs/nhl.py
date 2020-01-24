import json 
import discord
import requests
from tabulate import tabulate
from discord.ext import commands
from discord import Embed
from datetime import datetime
from pytz import timezone
import pytz
import humanize
#Game data found here
# https://statsapi.web.nhl.com/api/v1/game/{game id}/feed/live
DEBUG=False
"""
Title
ie BOS @ LVK
"""
def title_for_game(game):
    teams = game["gameData"]["teams"]
    away = teams["away"]["teamName"]
    home = teams["home"]["teamName"]
    return f"{away} @ {home}"

"""
Period of the game or 
Preview/Final/OT/SO
"""
def period_for_game(game):
    linescore = game["liveData"]["linescore"]
    period = linescore["currentPeriod"]
    if period > 0:
        periodstr = f"{linescore['currentPeriodTimeRemaining']} - {linescore['currentPeriodOrdinal']}"

    else:
        starttime = datetime.strptime(game["gameData"]["datetime"]["dateTime"], '%Y-%m-%dT%H:%M:%SZ')
        starttime = pytz.utc.localize(starttime).astimezone(timezone('America/New_York'))
        periodstr = f"Upcoming at {starttime.strftime('%I:%M %p %Z')}"
    
    return periodstr

"""
Game status
clock / time to drop / winner
"""
def footer_for_game(game):
    pass

"""
Game Score
[("Away Team", "[goals]"), 
("Home Team", "[goals]")]
for final, winner goals = "`[goals]`"
"""
def set_score_for_game(embed, game):
    linescore = game["liveData"]["linescore"]
    period = linescore["currentPeriod"]
    done = game["gameData"]["status"]["detailedState"] == "Final"
    teams = game["gameData"]["teams"]
    awayshort = teams["away"]["abbreviation"]
    homeshort = teams["home"]["abbreviation"]
    awaylocation = teams["away"]["locationName"]
    homeloaction = teams["home"]["locationName"]
    starttime = datetime.strptime(game["gameData"]["datetime"]["dateTime"], '%Y-%m-%dT%H:%M:%SZ')
    leaderstr = "Starts"
    scorestr = humanize.naturaltime(starttime)
    if period > 0:
        homescore = linescore["teams"]["home"]["goals"]
        awayscore = linescore["teams"]["away"]["goals"]

        homescorestr = f"**{homescore}**" if done and homescore > awayscore else f"{homescore}"
        awayscorestr = f"**{awayscore}**" if done and awayscore > homescore else f"{awayscore}"

        embed.add_field(name=awayshort, value=awayscorestr, inline=True)
        # embed.add_field(name="•", value="•", inline=True)
        embed.add_field(name=homeshort, value=homescorestr, inline=True)

        if homescore > awayscore:
            leaderstr = f"{homeloaction} {'won' if done else 'leads'}"
            scorestr = f"{homescore} - {awayscore}"
        elif awayscore > homescore:
            leaderstr = f"{awaylocation} {'won' if done else 'leads'}"
            scorestr = f"{awayscore} - {homescore}"
        else:
            leaderstr = "Game tied"
            scorestr = f"{awayscore} - {homescore}"
    
    embed.set_footer(text=f"{leaderstr} {scorestr}")

class NhlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    def show_game(self, gameId):
        url = f"https://statsapi.web.nhl.com/api/v1/game/{gameId}/feed/live"
        game = requests.get(url).json()
        embed = Embed(
            title=title_for_game(game), 
            description=period_for_game(game))
        set_score_for_game(embed, game)

        return embed
       
    #Creates the nhl command
    @commands.command(pass_context=True)
    async def nhl(self, ctx):
        
        #Grabs all the games that are playing for the day and stores it in a variable
        params = {'date': '2020-01-25'} if DEBUG else {}
        schedule = requests.get('https://statsapi.web.nhl.com/api/v1/schedule', params=params).json()
        # gameID = json.loads(gameID)

        #Iterates through all of the json data grabbing only the game ID numbers
        if len(schedule["dates"]) > 0 and len(schedule["dates"][0]["games"]) > 0:
        
            game_ids = [game["gamePk"] for game in schedule["dates"][0]["games"]]
            for id in game_ids:
                embed = self.show_game(id)
                await ctx.send(embed=embed)
        else:
            await ctx.send(embed=Embed(title="No Games Today"))

#This setup function is necessary otherwise this program will not be able to interact with the main
#bot file
def setup(bot):
    bot.add_cog(NhlCog(bot))
