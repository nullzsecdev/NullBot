#!/usr/lib/env python3

import re
import discord
import requests
import urllib.parse
from discord.ext import commands

"""
API Key can be obtained from here by registering for an account
"""
class UrlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Creating URL shortening command    
    @commands.command(pass_context=True)
    async def url(self, ctx, payload):
    
        url = "https://url-shortener-service.p.rapidapi.com/shorten"
        
        #URL encodes the given url so it can be read by the shortener
        payload = urllib.parse.quote(payload, safe='')
        
        newPayload = "url=" + payload
        headers = {
            'x-rapidapi-host': "url-shortener-service.p.rapidapi.com",
            'x-rapidapi-key': "8f96d7eab1msh279195b671b2e69p1d1a58jsn6157309cb10c",
            'content-type': "application/x-www-form-urlencoded"
            }
        #Sends the POST request to the website creating the shortened URL
        response = requests.request("POST", url, data=newPayload, headers=headers)
        
        #Extracts the URL from the recieved output
        shorten = response.text
        shorten = shorten.replace('\\', '')
        shorten = re.search("(?P<url>https?://[^\s]+)", shorten).group("url")
        shorten = shorten[:-2]
        
        #Prints the URL 
        await ctx.send(shorten)
        
#This setup function is necessary otherwise this program will not be able to interact with the main
#bot file
def setup(bot):
    bot.add_cog(UrlCog(bot))