#!/usr/bin/env python3
# Written by 3nt3r <--Thats me

import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

#Loads Discord token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

#Lets you know the bot has successfully logged in
@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + " " + str(bot.user.id))

#Prints this welcome message when a new user joins the server
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

#Command is the output of the '!help' command
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="NullBot", description="List of Commands:")
    
    embed.add_field(name="List of Various Resources", value="!Resources", inline=False)
    embed.add_field(name="Various Mod Commands", value="!Mod", inline=False)
    embed.add_field(name="Display this Message", value="!help", inline=False)

    await ctx.send(embed=embed)

bot.run(token)
