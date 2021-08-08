import discord
from discord.ext import commands, tasks
import random
import asyncio


#
#this file here contains most useful commands that don't need special permissions
#

class Usercommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #modmail
    @commands.command()
    async def modmail(self, ctx, *, args):
        if str(ctx.channel.type) == 'private': #only works in dm's
            guild = self.bot.get_guild(739299507795132486) #ssbu tg server
            modmail_channel = self.bot.get_channel(806860630073409567) #modmail channel
            mod_role = discord.utils.get(guild.roles, id=739299507816366106)
            atm = ''
            if ctx.message.attachments:
                atm = ", ".join([i.url for i in ctx.message.attachments])
            await modmail_channel.send(f"**✉️ New Modmail {mod_role.mention}! ✉️**\nFrom: {ctx.author} \nMessage:\n{args} \n{atm}")
            await ctx.send("Your message has been sent to the Moderator Team. They will get back to you shortly.")


        else:
            await ctx.message.delete()
            await ctx.send("For the sake of privacy, please only use this command in my DM's. They are always open for you.")
    

    #just returns the avatar of a user
    @commands.command(aliases=['icon'])
    async def avatar(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.avatar.url)

    #makes a basic poll
    @commands.command()
    async def poll(self, ctx, question, *options: str):
        if len(options) < 2:
            await ctx.send("You need at least 2 options to make a poll!") #obviously
            return
        if len(options) > 10:
            await ctx.send("You can only have 10 options at most!") #reaction emoji limit
            return
        try:
            await ctx.message.delete()
        except:
            pass

        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','0️⃣'] #in order
        description = []

        for x, option in enumerate(options):
            description += f'\n{reactions[x]}: {option}' #adds the emoji: option to the embed
        embed = discord.Embed(title=question, description=''.join(description), colour=discord.Colour.dark_purple())
        embed.set_footer(text=f'Poll by {ctx.author}')
        embed_message = await ctx.send(embed=embed) #sends the embed out
        for reaction in reactions[:len(options)]: #and then reacts with the correct number of emojis
            await embed_message.add_reaction(reaction)


    #pic with our stagelist on it, change file when it changes
    @commands.command()
    async def stagelist(self, ctx):
        await ctx.send(file=discord.File(r"/root/tabuu bot/files/stagelist.png")) 

    #classic ping
    @commands.command()
    async def ping(self, ctx):
        pingtime=self.bot.latency * 1000
        await ctx.send(f"Ping: {round(pingtime)}ms")

    #invite link
    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Here's the invite link to our server: https://discord.gg/ssbutg") #if this link expires, change it

    #coaching info
    @commands.command()
    async def coaching(self, ctx):
        await ctx.send("It seems like you are looking for coaching: make sure to tell us what exactly you need so we can best assist you!\n\n1. Did you specify which character you need help with?\n2. Are you looking for general advice, character-specific advice, both?\n3. How well do you understand general game mechanics on a scale of 1-5 (1 being complete beginner and 5 being knowledgeable)?\n4. Region?\n5. What times are you available?\n\nPlease keep in mind if you are very new to the game or have a basic understanding, it is recommended to first learn more via resources like Izaw's Art of Smash series (which you can find on YouTube) or other resources we have pinned in <#739299508403437621>.")

    #links to our calendar
    @commands.command(aliases=['calender', 'calandar', 'caIendar'])
    async def calendar(self, ctx): #the basic schedule for our server
        await ctx.send("https://calendar.google.com/calendar/embed?src=ssbu.traininggrounds%40gmail.com&ctz=America%2FNew_York")

    #generic coin toss
    @commands.command()
    async def coin(self, ctx):
        coin = ['Coin toss: **Heads!**', 'Coin toss: **Tails!**']
        await ctx.send(random.choice(coin))

    #neat dice roll
    @commands.command(aliases=['r'])
    async def roll(self, ctx, dice:str):
        try:
            amount, sides = map(int, dice.split('d'))
        except:
            await ctx.send("Wrong format!\nTry something like: %roll 1d100")
            return
        results = []
        if amount > 100:
            await ctx.send("Too many dice!")
            return
        if sides > 1000:
            await ctx.send("Too many sides!")
            return
        for r in range(amount):
            x = random.randint(1, sides)
            results.append(x)
        if len(results) == 1:
            await ctx.send(f"Rolling **1**-**{sides}** \nResult: **{results}**")
        else:
            await ctx.send(f"Rolling **1**-**{sides}** **{r+1}** times \nResults: **{results}** \nTotal: **{sum(results)}**")

    #generic countdown
    @commands.command()
    async def countdown(self, ctx, count:int):
        if count > 50:
            await ctx.send("Please don't use numbers that big.")
            return
        if count < 1:
            await ctx.send("Invalid number!")
            return
        
        initial_count = count

        countdown_message = await ctx.send(f"Counting down from {initial_count}...\n{count}")

        while count > 1:
            count -= 1
            await asyncio.sleep(2) #sleeps 2 secs instead of 1
            await countdown_message.edit(content=f"Counting down from {initial_count}...\n{count}") #edits the message with the new count

        await asyncio.sleep(2) #sleeps again before sending the final message
        await countdown_message.edit(content=f"Counting down from {initial_count}...\nFinished!")

    #reminder, just waits out the time, no fancy stuff
    @commands.command(aliases=['remindme'])
    async def reminder(self, ctx, time, *, remind_message):
        #this here gets the time
        if time.lower().endswith("d"):
            seconds = int(time[:-1]) * 60 * 60 * 24
            reminder_time = f"{seconds // 60 // 60 // 24} day(s)"
        elif time.lower().endswith("h"):
            seconds = int(time[:-1]) * 60 * 60
            reminder_time = f"{seconds // 60 // 60} hour(s)"
        elif time.lower().endswith("m"):
            seconds = int(time[:-1]) * 60
            reminder_time = f"{seconds // 60} minute(s)"
        elif time.lower().endswith("s"):
            seconds = int(time[:-1])
            reminder_time = f"{seconds} seconds"
        else:
            await ctx.send("Invalid time format! Please use a number followed by d/h/m/s for days/hours/minutes/seconds.")
            return
        
        if seconds < 30:
            await ctx.send("Duration is too short! I'm sure you can remember that yourself.")
            return
        if seconds > 2592000: #30 days
            await ctx.send("Duration is too long! Maximum duration is 30 days.")
            return

        await ctx.send(f"{ctx.author.mention}, I will remind you about `{remind_message}` in {reminder_time}!")

        await asyncio.sleep(seconds) #bit flawed, if i restart the bot obviously the reminders get deleted, would work better if i would store them in a json file but oh well

        await ctx.send(f"{ctx.author.mention}, you wanted me to remind you of `{remind_message}`, {reminder_time} ago.")

    #info about an emoji
    @commands.command(aliases=['emoji'])
    async def emote(self, ctx, emoji:discord.PartialEmoji):
        embed = discord.Embed(title="Emoji Info", colour=discord.Colour.orange(), description=f"\
**Url:** {emoji.url}\n\
**Name:** {emoji.name}\n\
**ID:** {emoji.id}\n\
**Created at:** {str(emoji.created_at).split('.')[0]} CET\n\
            ")
        embed.set_image(url=emoji.url)
        await ctx.send(embed=embed)

    #returns the spotify status
    @commands.command()
    async def spotify(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author

        if not ctx.guild:
            await ctx.send("This command does not work in my DM channel.")
            return

        listeningstatus = next((activity for activity in member.activities if isinstance(activity, discord.Spotify)), None)

        if listeningstatus is None:
            await ctx.send("This user is not listening to Spotify right now or their account is not connected.")
        else:
            await ctx.send(f"https://open.spotify.com/track/{listeningstatus.track_id}")



    #our streamers use these shortcuts to promote their streams
    @commands.command()
    async def streamer(self, ctx):
        await ctx.send("Streamer commands: \n%neon, %scrooge, %tabuu, %xylenes, %tgstream") #needs updating every once in a while

    @commands.command()
    async def neon(self, ctx):
        await ctx.send("https://www.twitch.tv/neonsurvivor")

    @commands.command()
    async def scrooge(self, ctx):
        await ctx.send("https://www.twitch.tv/scroogemcduk")
    
    @commands.command()
    async def tabuu(self, ctx):
        await ctx.send("https://www.twitch.tv/therealtabuu")

    @commands.command()
    async def xylenes(self, ctx):
        await ctx.send("https://www.twitch.tv/FamilyC0mputer")

    @commands.command()
    async def tgstream(self, ctx):
        await ctx.send("https://www.twitch.tv/ssbutraininggrounds")





    #error handling for the above
    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member, or just leave it blank.")
        else:
            raise error

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a question, and then at least 2 options!")
        else:
            raise error


    @modmail.error
    async def modmail_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a message to the moderators. It should look something like:\n```%modmail (your message here)```")
        else:
            raise error

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Wrong format!\nTry something like: %roll 1d100")
        else:
            raise error

    @countdown.error
    async def countdown_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to input a number!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid number!")
        else:
            raise error

    @reminder.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify an amount of time and the reminder message!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("Invalid time format! Please use a number followed by d/h/m/s for days/hours/minutes/seconds.")
        else:
            raise error

    @emote.error
    async def emote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify an emoji!")
        elif isinstance(error, commands.PartialEmojiConversionFailure):
            await ctx.send("I couldn't find information on this emoji! Make sure this is not a default emoji.")
        else:
            raise error

    @spotify.error
    async def spotify_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member, or just leave it blank.")
        else:
            raise error



def setup(bot):
    bot.add_cog(Usercommands(bot))
    print("Usercommands cog loaded")