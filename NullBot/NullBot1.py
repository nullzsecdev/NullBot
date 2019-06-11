import discord

client = discord.Client()
#Reads API token from file
token = open('token.txt', 'r').readline()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #Opens a list of curse words
    words = open("cursewords.txt", "r")
    for curse in words:
        if message.content.count(curse) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Do you talk to your mother like that")

    #Counts he number of members in the server
    counter = 0
    for member in client.get_all_members():
        counter += 1

    channels =["devs", "bot-test"]
    
    #Help commands
    if message.content == "!help":
        embed = discord.Embed(title="Bot Help", description="Bot Commands")
        embed.add_field(name="!hello", value="Greets the user")
        embed.add_field(name="!users", value="Number of Users")
        embed.add_field(name="!HTB", value="HTB Link")
        embed.add_field(name="!resources", value="List of Resources")
        await message.channel.send(content=None, embed=embed)
    
    #What each help command does
    if message.content.find("!hello") != -1:
        await message.channel.send("Hello")
    elif message.content == "!users":
        await message.channel.send("Number of Members: " + str(counter))
    elif message.content == "!HTB":
        await message.channel.send("https://www.hackthebox.eu/")
    elif message.content == "!resources":
        resources = open('resources.txt', 'r')
        for line in resources:
            await message.channel.send(str(line))


client.run(token.strip())
