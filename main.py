#Tabuu 3.0
#by Phxenix for SSBU Training Grounds
#Version: 4.2.1
#Last Changes: 9 August 2021
#Report any bugs to: Phxenix#1104
#
#To do list:
#- ask for command ideas & new statuses


import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio
import os


#
#this main file here loads all the cogs and starts the bot obviously, also includes our custom help command as a sort of glossary
#

intents=intents=discord.Intents.all() #intents so the bot can track its users
bot = Bot(command_prefix='%', intents=intents) # prefix for commands, we picked %, intents same as above
client = discord.Client(intents=intents) 
bot.remove_command('help') #for a custom help command

bot.version_number = "4.2.1" #the "version", maintain every now and then


#bot startup, and some event triggers without commands
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print ("Lookin' good, connected as", bot.user) #prints to the console that its ready



#help command, to tidy things up a bit i broke it into subcommands
@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Help menu, available subcommands:", colour=0x007377, description='\n\
`%help admin` - Moderation commands\n\
`%help info` - Informational commands\n\
`%help mm` - Matchmaking commands\n\
`%help util` - Utility commands\n\
`%help misc` - Miscellaneous commands\n\
`%help fun` - Fun commands\n\
        ')
    await ctx.send(embed=embed)


#the subcommands, mentioned above
@help.command()
@commands.has_permissions(administrator=True) #only making these visible for the mods
async def admin(ctx):
    embed = discord.Embed(title = "💻Admin Commands💻", color=0xff0000, description='\n\
```%ban <@user> <reason>``` - Bans a member from the server.\n\
```%unban <@user>``` - Revokes a ban from the server.\n\
```%kick <@user> <reason>``` - Kicks a user from the server.\n\
```%clear <amount>``` - Purges X messages from the channel (default:1).\n\
```%delete <message IDs>``` - Deletes certain messages by ID.\n\
```%mute <@user> <reason>``` - Mutes a user in the server.\n\
```%unmute <@user>``` - Unmutes a user in the server.\n\
```%tempmute <@user> <time> <reason>``` - Temporarily mutes a user.\n\
```%addrole <@user> <role>``` - Adds a role to a user.\n\
```%removerole <@user> <role>``` - Removes a role from a User.\n\
```%warn <@user> <reason>``` - Warns a user.\n\
```%warndetails <@user>``` - Shows detailed warnings of a user. \n\
```%deletewarn <@user> <warn_id>``` - Deletes a specific warning.\n\
```%clearwarns <@user>``` - Clears all the warnings of a user.\n\
```%clearmmpings``` - Clears all matchmaking pings.\n\
```%records``` - Shows ban records.\n\
```%forcereportmatch <@winner> <@loser>``` - If someone abandons a ranked match.\n\
```%leaderboard``` - Leaderboards of ranked matchmaking\n\
```%newrolemenu <message ID> <emoji> <role>``` - Adds an entry for a role menu.\n\
```%deleterolemenu <message ID>``` - Deletes every entry for a Message with a role menu.\n\
```%modifyrolemenu <message ID> <exclusive> <Optional Role>``` - Sets special permissions for a Role menu.\n\
```%geteveryrolemenu``` - Gets you every role menu entry currently active.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')

@help.command()
async def info(ctx):
    embed = discord.Embed(title="❓Info Commands❓", color=0x06515f, description='\n\
```%roleinfo <role>``` - Displays Role info.\n\
```%listrole <role>``` - Displays all the members with a certain Role.\n\
```%userinfo <member>``` - Shows user info of a mentioned member.\n\
```%warns <@user>``` - Displays the number of warnings of a user.\n\
```%server``` - Info about the server.\n\
```%stats``` - Stats about the bot.\n\
```%emote <emoji>``` - Info about an emoji.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')

@help.command()
async def mm(ctx):
    embed = discord.Embed(title="⚔️Matchmaking Commands⚔️", color=0x420202, description='\n\
```%singles``` - Used for 1v1 matchmaking in our arena channels.\n\
```%doubles``` - Used for 2v2 matchmaking in our arena channels.\n\
```%funnies``` - Used for non-competitive matchmaking in our arena channels.\n\
```%recentpings <type>``` - Gets you the recent pings of any matchmaking type.\n\
```%rankedmm``` - Used for 1v1 ranked matchmaking in our ranked channels.\n\
```%reportmatch <@user>``` - Winner of the set reports the result, <@user> being the person you won against.\n\
```%rankedstats``` - Your ranked stats.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')

@help.command()
async def util(ctx):
    embed = discord.Embed(title="🔧Utility Commands🔧", color=0x424242, description='\n\
```%coin``` - Throws a coin\n\
```%roll <NdN>``` - Rolling dice, format %roll 1d100.\n\
```%countdown <number>``` - Counts down from number.\n\
```%poll <"question"> <"option 1"> <"option 2">``` - Starts a poll with a maximum of 10 choices.\n\
```%reminder <time> <message>``` - Reminds you about something.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')


@help.command()
async def misc(ctx):
    embed = discord.Embed(title="📋Miscellaneous Commands📋", color=0x155a00, description='\n\
```%modmail <your message>``` - A private way to communicate with the moderator team. Only works in my DM channel.\n\
```%updatelevel``` - Updates your level role manually.\n\
```%stagelist``` - Our Stagelist for Crew Battles.\n\
```%coaching``` - Coaching requirements.\n\
```%calendar``` - Calendar with our schedule.\n\
```%invite``` - For those looking for an invite.\n\
```%icon <@user>``` - Gets you the avatar of a user.\n\
```%spotify <@user>``` - Posts the song the user is currently streaming.\n\
```%<streamer>``` - Links to one of our streamers.\n\
```%ping``` - Gets the ping of the bot.\n\
```%mp4<move>``` - Tells you the Mana Cost of any of Hero\'s moves.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')


@help.command()
async def fun(ctx):
    embed = discord.Embed(title="😂Fun Commands😂", color=0x841e8b, description='\n\
```%joke``` - Jokes.\n\
```%randomquote``` - Quotes.\n\
```%pickmeup``` - Nice words.\n\
```%wisdom``` - It\'s wisdom.\n\
```%boo``` - Looking for a scare, huh?\n\
```%uwu``` - For the silly people.\n\
```%tabuwu``` - For the dumb people.\n\
```%john``` - If you need a john.\n\
```%8ball <question>``` - Ask the magic 8-ball.\n\
```%who <question>``` - Ask a question and get a random user in response.\n\
        ')
    await ctx.author.send(embed=embed)
    await ctx.message.add_reaction('👍')



#error handling for the admin subcommand
@admin.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You are not a moderator on this server.")
    else:
        raise error



    
#loads all of our cogs
for filename in os.listdir(r'/root/tabuu bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


#run token, in different file because of security
with open(r'/root/tabuu bot/files/token.txt') as f:
    TOKEN = f.readline()

bot.run(TOKEN)