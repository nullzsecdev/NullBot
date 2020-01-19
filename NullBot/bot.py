#!/usr/bin/env python3
# Written by 3nt3r <--Thats me
import os

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + " " + str(bot.user.id))

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "welcome":
            await channel.send(f"""Hi {member.mention}, welcome to the NullzSec server!
Please introduce yourself by possibly answering a few questions.
1. What brings you to the server?
2. Do you have any previous experience, whether it be with linux, or hacking in general?
3. Are you a student or do you work in the field, or maybe this is just a hobby?
4. What is your first pets name?
5. Whats your SSN?
6. Whats your mothers maiden name?""")

bot.remove_command('help')

@bot.command()
async def linuxPrivEsc(ctx):
    with open("linuxPrivEsc.txt","r") as f:
        priv = f.read()
        await ctx.send(priv)

@bot.command()
async def windozePrivEsc(ctx):
    with open("windozePrivEsc.txt","r") as f:
        priv = f.read()
        await ctx.send(priv)

@bot.command()
async def youtube(ctx):
    with open("youtube.txt","r") as f:
        video = f.read()
        await ctx.send(video)

@bot.command()
async def reddit(ctx):
    with open("reddit.txt","r") as f:
        subreddit = f.read()
        await ctx.send(subreddit)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Proto Bot", description="List of Commands:", color=0xf7e6d4)
    
    embed.add_field(name="!linuxPrivEsc", value="Resources for Linux Privilesge escalation", inline=False)
    embed.add_field(name="!windozePrivEsc", value="Resources for Windoze Priviledge escalation", inline=False)
    embed.add_field(name="!youtube", value="Usefule youtube channels", inline=False)
    embed.add_field(name="!reddit", value="Useful subreddits", inline=False)
    embed.add_field(name="!HTBhint", value="Hints for various HTB boxes", inline=False)
    embed.add_field(name="!help", value="Displays this message", inline=False)

    await ctx.send(embed=embed)


bot.run(token)
