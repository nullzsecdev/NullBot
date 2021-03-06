#!/usr/bin/env python3
# Written by 3nt3r <--Thats me

import os
import sys
import discord
import traceback
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

#Loads Discord token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

#List of different cogs imported
initial_extensions = ['cogs.nhl',
                      'cogs.google',
                      'cogs.url']

#Iterates through the lists of cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extentsion {extension}.',file=sys.stderr)
            traceback.print_exc()
            
#Lets you know the bot has successfully logged in
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + " " + str(bot.user.id))

#Prints this welcome message when a new user joins the server
@bot.event
async def on_member_join( member):

    embed = discord.Embed(title="Welcome to the Nullzsec Discord Server!", description="""This server was created to mainly bring together people who are interested in hacking. Whether you are just beginning your journey or a seasoned veteran, all are welcome. Please make sure to take a quick look at the #rules.

            Before you can access the rest of the channel's, you must become a member. You can do this by typing '!member' in this chat and a the next available Mod will make you a member. Please be patient as response times may vary since we are not available 24/7.

            This bot has some commands that you can use and can be listed by typing '!help'. It is still a work in progress so functionality is limited at the moment.""")
    await member.create_dm()
    await member.dm_channel.send(embed=embed)

#removes the 'help' command so it can be added to the list of commands
bot.remove_command('help')

#List of commands that a Admins and Moderators are able to run
@bot.command()
@has_permissions(kick_members=True, ban_members=True, change_nickname=True)
async def Mod(ctx):
    embed = discord.Embed(title="NullBot", description="Moderator Commands:")

    embed.add_field(name="Kick a member", value="!kick <member>", inline=False)
    embed.add_field(name="Ban a member", value="!ban <member>", inline=False)
    embed.add_field(name="Unban a member", value="!unban <member>", inline=False)
    embed.add_field(name="Add a role to a member", value="!addrole <member> <role>", inline=False)
    embed.add_field(name="Remove a role from a member", value='!remrole <member> <role>', inline=False)
    embed.add_field(name="Send an announcement with @everyone", value="!announce <message>", inline=False)
    embed.add_field(name="Set the nickname of a member", value="!nick <member> <nickname>", inline=False)

    await ctx.send(embed=embed)

#List of commands with links to resources for various topics, all members can access these
@bot.command()
async def Resources(ctx):
    embed = discord.Embed(title="NullBot", description="List of Resources")

    embed.add_field(name="Resources for Linux Priv Esc", value="!linuxPrivEsc", inline=False)
    embed.add_field(name="Resources for Windows Priv Esc", value="!windowsPrivEsc", inline=False)
    embed.add_field(name="Usefule Youtube Channels", value="!youtube", inline=False)
    embed.add_field(name="Usefull subreddits", value="!reddit", inline=False)
    embed.add_field(name="Hints for various HTB Boxes", value="!HTBhints", inline=False)

    await ctx.send(embed=embed)

#Command to kick members
@bot.command(pass_context=True)
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

#Command to Ban members
@bot.command(pass_contents=True)
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)

#Command to Unban members
@bot.command(pass_contents=True)
@has_permissions(ban_members=True)
async def unban(ctx, member : discord.Member, *, reason=None):
    await member.unban(reason=reason)

#Command to change the nickname of another member
@bot.command(pass_context=True)
@has_permissions(manage_nicknames=True)
async def nick(ctx, member : discord.Member, *, nickname, reason=None):
    await member.edit(nick=nickname)

#Command to add a role to another member
@bot.command(pass_context=True)
@has_permissions(manage_roles=True)
async def addrole(ctx, member : discord.Member, *role : discord.Role, reason=None):
    await member.add_roles(*role)

#Command to remove a role from a member
@bot.command(pass_context=True)
@has_permissions(manage_roles=True)
async def remrole(ctx, member : discord.Member, *role: discord.Role, reason=None):
    await member.remove_roles(*role)

#Command outputs Linux Priv Esc resources by reeading them from file
@bot.command()
async def linuxPrivEsc(ctx):
    with open("linuxPrivEsc.txt","r") as f:
        priv = f.read()
        await ctx.send(priv)

#Command outputs Windows Priv Esc resources by reading them from file
@bot.command()
async def windowsPrivEsc(ctx):
    with open("windozePrivEsc.txt","r") as f:
        priv = f.read()
        await ctx.send(priv)

#command outputs Youtube channels by reading them from file
@bot.command()
async def youtube(ctx):
    with open("youtube.txt","r") as f:
        video = f.read()
        await ctx.send(video)

#command outputs various subreddits by reading them from file
@bot.command()
async def reddit(ctx):
    with open("reddit.txt","r") as f:
        subreddit = f.read()
        await ctx.send(subreddit)

#Command that sends a message to the mods private channel to give the new member the member role
@bot.command()
@commands.dm_only()
async def member(ctx):
    channel = bot.get_channel(586725273173622796)
    if channel:
        await channel.send("{} needs to be made a member.".format(ctx.message.author.mention))

#Error handling for the member command    
@member.error
async def member_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('Command not valid here, please send it to me in a DM.')

#Command is the output of the '!help' command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="NullBot", description="List of Commands:")
    
    embed.add_field(name="List of Various Resources", value="!Resources", inline=False)
    embed.add_field(name="Various Mod Commands", value="!Mod", inline=False)
    embed.add_field(name="Get scores for the days NHL games", value="!nhl", inline=False)
    embed.add_field(name="Search google and get top result", value="!google \"<search>\"", inline=False)
    embed.add_field(name="Display this Message", value="!help", inline=False)

    await ctx.send(embed=embed)

bot.run(token)

