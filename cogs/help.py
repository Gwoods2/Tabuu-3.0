import discord
from discord.ext import commands, tasks

#
#this file here contains the dropdown menu for our help command, to be renamed for use
#


class Responses(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Admin', description='Admin Commands', emoji='💻'),
            discord.SelectOption(label='Info', description='Informational Commands', emoji='❓'),
            discord.SelectOption(label='Matchmaking', description='Matchmaking Commands', emoji='⚔️'),
            discord.SelectOption(label='Utility', description='Utility Commands', emoji='🔧'),
            discord.SelectOption(label='Miscellaneous', description='Miscellaneous Commands', emoji='📋'),
            discord.SelectOption(label='Fun', description='Fun Commands', emoji='😂')
        ]

        super().__init__(placeholder='What do you need help with?', min_values=1, max_values=1, options=options)


    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Admin':
            if interaction.permissions.administrator is True:
                admin_embed = discord.Embed(title = "💻Admin Commands💻", color=0xff0000, description='\n\
```%ban <@user> <reason>``` - Bans a member from the server.\n\
```%unban <@user>``` - Revokes a ban from the server.\n\
```%kick <@user> <reason>``` - Kicks a user from the server.\n\
```%clear <amount>``` - Purges X messages from the channel (default:1)\n\
```%delete <message IDs>``` - Deletes certain messages by ID\n\
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
```%leaderboard``` - Leaderboards of ranked matchmaking.\n\
```%newrolemenu <message ID> <emoji> <role>``` - Adds an entry for a role menu.\n\
```%deleterolemenu <message ID>``` - Deletes every entry for a Message with a role menu.\n\
```%modifyrolemenu <message ID> <exclusive> <Optional Role>``` - Sets special permissions for a Role menu.\n\
```%geteveryrolemenu``` - Gets you every role menu entry currently active.\n\
```%reloadcogs``` - Owner only, reloads all of the modules of this bot.\n\
        ')
                await interaction.response.send_message(embed=admin_embed, ephemeral=True)
            else:
                await interaction.response.send_message("Sorry, you are not an administrator on this server!", ephemeral=True)

        elif self.values[0] == 'Info':
            info_embed = discord.Embed(title="❓Info Commands❓", color=0x06515f, description='\n\
```%roleinfo <role>``` - Displays Role info.\n\
```%listrole <role>``` - Displays all the members with a certain Role.\n\
```%userinfo <member>``` - Shows user info of a mentioned member.\n\
```%warns <@user>``` - Displays the number of warnings of a user.\n\
```%server``` - Info about the server.\n\
```%stats``` - Stats about the bot.\n\
```%emote <emoji>``` - Info about an emoji.\n\
```%sticker <sticker>``` - Info about a sticker.\n\
        ')
            await interaction.response.send_message(embed=info_embed, ephemeral=True)

        elif self.values[0] == 'Matchmaking':
            matchmaking_embed = discord.Embed(title="⚔️Matchmaking Commands⚔️", color=0x420202, description='\n\
```%singles``` - Used for 1v1 matchmaking in our arena channels.\n\
```%doubles``` - Used for 2v2 matchmaking in our arena channels.\n\
```%funnies``` - Used for non-competitive matchmaking in our arena channels.\n\
```%recentpings``` - Gets you the recent pings of any matchmaking type.\n\
```%rankedmm``` - Used for 1v1 ranked matchmaking in our ranked channels.\n\
```%reportmatch <@user>``` - Winner of the set reports the result, <@user> being the person you won against.\n\
```%rankedstats``` - Your ranked stats.\n\
        ')
            await interaction.response.send_message(embed=matchmaking_embed, ephemeral=True)

        elif self.values[0] == 'Utility':
            utility_embed = discord.Embed(title="🔧Utility Commands🔧", color=0x424242, description='\n\
```%coin``` - Throws a coin\n\
```%roll <NdN>``` - Rolling dice, format %roll 1d100.\n\
```%countdown <number>``` - Counts down from number.\n\
```%poll <"question"> <"option 1"> <"option 2">``` - Starts a poll with a maximum of 10 choices.\n\
```%reminder <time> <message>``` - Reminds you about something.\n\
        ')
            await interaction.response.send_message(embed=utility_embed, ephemeral=True)

        elif self.values[0] == 'Miscellaneous':
            miscellaneous_embed = discord.Embed(title="📋Miscellaneous Commands📋", color=0x155a00, description='\n\
```%modmail <your message>``` - A private way to communicate with the moderator team. Only works in my DM channel.\n\
```%updatelevel``` - Updates your level role manually.\n\
```%stagelist``` - Our Stagelist for Crew Battles.\n\
```%coaching``` - Coaching requirements.\n\
```%calendar``` - Calendar with our schedule.\n\
```%pr``` - Links to the PR of our tourneys.\n\
```%resources``` - Our resource document for new players.\n\
```%invite``` - For those looking for an invite.\n\
```%avatar <@user>``` - Gets you the avatar of a user.\n\
```%banner <@user>``` - Gets you the banner of a user.\n\
```%spotify <@user>``` - Posts the song the user is currently streaming.\n\
```%<streamer>``` - Links to one of our streamers.\n\
```%ping``` - Gets the ping of the bot.\n\
```%mp4<move>``` - Tells you the Mana Cost of any of Hero\'s moves.\n\
        ')
            await interaction.response.send_message(embed=miscellaneous_embed, ephemeral=True)
        
        elif self.values[0] == 'Fun':
            fun_embed = discord.Embed(title="😂Fun Commands😂", color=0x841e8b, description='\n\
```%joke``` - Jokes\n\
```%randomquote``` - Quotes\n\
```%pickmeup``` - Nice words\n\
```%wisdom``` - It\'s wisdom\n\
```%boo``` - Looking for a scare, huh?\n\
```%uwu``` - For the silly people\n\
```%tabuwu``` - For the dumb people\n\
```%john``` - If you need a john\n\
```%8ball <question>``` - Ask the magic 8-ball.\n\
```%who <question>``` - Ask a question and get a random user in response.\n\
        ')
            await interaction.response.send_message(embed=fun_embed, ephemeral=True)

        else:
            await interaction.response.send_message("Something went wrong! Please try again.", ephemeral=True)
        


class DropdownHelp(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Responses())


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        await ctx.send("Here are the available subcommands:", view=DropdownHelp())



def setup(bot):
    bot.add_cog(Help(bot))
    print("Help cog loaded")