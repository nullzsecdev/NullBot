#!/usr/bin/env python3

import discord
from googlesearch import search
from discord.ext import commands

class GoogleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Create the google command
    @commands.command(pass_context=True)
    async def google(self, ctx, query):

        #Searches google and returns only the top result
        for j in search(query, tld="com", num=1,stop=1,pause=2):
            await ctx.send(j)

#This setup function is necessary otherwise this program will not be able to interact with the main
#bot file
def setup(bot):
    bot.add_cog(GoogleCog(bot))


