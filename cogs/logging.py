import discord
from discord.ext import commands
from io import StringIO
from utils.ids import GuildIDs, TGChannelIDs, BGChannelIDs


class Logging(commands.Cog):
    """
    Logs every little user update or message update into the logs channel.
    """

    def __init__(self, bot):
        self.bot = bot

    def get_logchannel(self, guild_id: int):
        """
        Gets you the correct Log Channel ID.
        """
        if guild_id == GuildIDs.TRAINING_GROUNDS:
            return TGChannelIDs.LOGCHANNEL
        elif guild_id == GuildIDs.BATTLEGROUNDS:
            return BGChannelIDs.LOGCHANNEL

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        # username change
        if before.name != after.name:
            embed = discord.Embed(
                title="**✏️ Username changed ✏️**",
                description=f"Before: {before.name}\nAfter: {after.name}",
                colour=discord.Colour.orange(),
            )
            embed.set_author(
                name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
            )
            embed.timestamp = discord.utils.utcnow()
            # we send the embed in every server that we have in common with the user
            for server in after.mutual_guilds:
                logs = self.bot.get_channel(self.get_logchannel(server.id))
                await logs.send(embed=embed)

        # discriminator change
        if before.discriminator != after.discriminator:
            embed = discord.Embed(
                title="**✏️ Discriminator changed ✏️**",
                description=f"Before: {before.discriminator}\nAfter: {after.discriminator}",
                colour=discord.Colour.orange(),
            )
            embed.set_author(
                name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
            )
            embed.timestamp = discord.utils.utcnow()
            for server in after.mutual_guilds:
                logs = self.bot.get_channel(self.get_logchannel(server.id))
                await logs.send(embed=embed)

        # avatar change
        if before.display_avatar.url != after.display_avatar.url:
            embed = discord.Embed(
                title=f"**📷 Avatar changed 📷**",
                description=f"New avatar below:",
                colour=discord.Colour.dark_gray(),
            )
            embed.set_thumbnail(url=before.display_avatar.url)
            embed.set_image(url=after.display_avatar.url)
            embed.set_author(
                name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
            )
            embed.timestamp = discord.utils.utcnow()
            for server in after.mutual_guilds:
                logs = self.bot.get_channel(self.get_logchannel(server.id))
                await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # if someone changes their nickname on this server
        if before.display_name != after.display_name:
            embed = discord.Embed(
                title="**✏️ Nickname changed ✏️**",
                description=f"Before: {before.display_name}\nAfter: {after.display_name}",
                colour=discord.Colour.orange(),
            )
            embed.set_author(
                name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
            )
            embed.timestamp = discord.utils.utcnow()
            logs = self.bot.get_channel(self.get_logchannel(before.guild.id))
            await logs.send(embed=embed)

        # roles change
        if before.roles != after.roles:
            # user gains a role
            if len(before.roles) < len(after.roles):
                newRole = next(
                    role for role in after.roles if role not in before.roles
                )  # gets the new role
                embed = discord.Embed(
                    title="**📈 User gained role 📈**",
                    description=f"Role gained: {newRole.mention}",
                    colour=discord.Colour.green(),
                )
                embed.set_author(
                    name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
                )
                embed.timestamp = discord.utils.utcnow()
                logs = self.bot.get_channel(self.get_logchannel(before.guild.id))
                await logs.send(embed=embed)

            # user loses a role
            if len(before.roles) > len(after.roles):
                oldRole = next(
                    role for role in before.roles if role not in after.roles
                )  # gets the old role
                embed = discord.Embed(
                    title="**📉 User lost role 📉**",
                    description=f"Role lost: {oldRole.mention}",
                    colour=discord.Colour.dark_red(),
                )
                embed.set_author(
                    name=f"{str(after)} ({after.id})", icon_url=after.display_avatar.url
                )
                embed.timestamp = discord.utils.utcnow()
                logs = self.bot.get_channel(self.get_logchannel(before.guild.id))
                await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="**🎆 New member joined 🎆**",
            description=f"{member.mention} has joined the server!\n\n**Account created:**\n{discord.utils.format_dt(member.created_at, style='R')}",
            colour=discord.Colour.green(),
        )
        embed.set_author(
            name=f"{str(member)} ({member.id})", icon_url=member.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(member.guild.id))
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # @everyone is considered a role too, so we remove that from the list
        everyonerole = discord.utils.get(member.guild.roles, name="@everyone")
        roles = [role.mention for role in member.roles if role is not everyonerole]
        # users may leave without a role to their name (except @everyone i guess)
        role_description = f"{' '.join(roles)}" if len(roles) != 0 else "No roles"

        embed = discord.Embed(
            title=f"** 🚶 Member left the server 🚶**",
            description=f"{member.mention} has left the server. \n**Lost roles:** \n{role_description}",
            colour=discord.Colour.dark_red(),
        )
        embed.set_author(
            name=f"{str(member)} ({member.id})", icon_url=member.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(member.guild.id))
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # dont want dms to be included, same in the below listeners
        if not after.guild:
            return

        # also dont care about bot message edits
        if after.author.bot:
            return

        # sometimes the message content may be the same, so we skip that, too
        if before.content == after.content:
            return

        # discord released an update where they allow nitro users to send messages with up to 4000 chars in them
        # but an embed can only have 6000 chars in them
        # so we need to add in a check to not get dumb errors.
        # 2000 chars is still the limit for non-nitro users so it should be fine.
        if len(after.content[2000:]) > 0:
            after.content = "Content is too large to fit in a single embed."
        if len(before.content[2000:]) > 0:
            before.content = "Content is too large to fit in a single embed."

        # if you send an empty message and then edit it (like when you upload pics), the before field cannot be empty
        if len(before.content) == 0:
            before.content = "\u200b"

        embed = discord.Embed(
            title=f"**✍️ Edited Message in {after.channel.name}! ✍️**",
            description=f"**New Content:**\n{after.content}",
            colour=discord.Colour.orange(),
        )
        embed.set_author(
            name=f"{str(after.author)} ({after.author.id})",
            icon_url=after.author.display_avatar.url,
        )
        embed.add_field(
            name=f"**Old Content:**", value=f"{before.content[:1000]}", inline=False
        )
        # if a message is too long, it gets split into two embed fields
        # 1000 chars is the limit for embed values
        if len(before.content[1000:]) > 0:
            embed.add_field(
                name="(Continued from above)", value=before.content[1000:], inline=False
            )
        embed.add_field(name="Message ID:", value=f"{after.id}\n{after.jump_url}")
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(before.guild.id))
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild:
            return

        if message.author.bot:
            return

        embed = discord.Embed(
            title=f"**❌ Deleted Message in {message.channel.name}! ❌**",
            description=f"**Content:**\n{message.content}",
            colour=discord.Colour.dark_red(),
        )
        embed.set_author(
            name=f"{str(message.author)} ({message.author.id})",
            icon_url=message.author.display_avatar.url,
        )
        # if a message has an attachment with it, it also gets logged. i dont really care for that on the on message edit though
        if message.attachments:
            # for one attachment, this is enough
            if len(message.attachments) == 1:
                if message.attachments[0].url.endswith(
                    (".jpg", ".png", ".jpeg", ".gif")
                ):
                    new_url = message.attachments[0].url.replace(
                        "cdn.discordapp.com", "media.discordapp.net"
                    )
                    embed.set_image(url=new_url)
                    embed.add_field(
                        name="Attachment:", value="See below.", inline=False
                    )
                else:
                    embed.add_field(
                        name="Attachment:",
                        value=message.attachments[0].url,
                        inline=False,
                    )
            # for multiple, putting it all into one embed value might result in too many characters, so this is needed
            else:
                i = 1
                for x in message.attachments:
                    embed.add_field(
                        name=f"Attachment ({i}/{len(message.attachments)}):",
                        value=x.url,
                        inline=False,
                    )
                    i += 1

        if message.stickers:
            # so as far as i know, you can only have 1 sticker attached to a message
            # but you can have 1 sticker and some other attachments
            if not message.attachments:
                embed.set_image(url=message.stickers[0].url)
                embed.add_field(name="Sticker:", value="See below.", inline=False)
            else:
                embed.add_field(name="Sticker:", value=f"{message.stickers[0].url}")

        embed.add_field(name="Message ID:", value=message.id)
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(message.guild.id))
        # as far as i can tell, the maximum message possible with 4k chars + 10 attachments + 1 sticker just barely fits in one embed
        # the limit for embeds are 6k chars total. so we might wanna keep watching this in case of errors.
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        # defines the embed
        embed = discord.Embed(
            title=f"**❌ Bulk message deletion in {messages[0].channel.name}! ❌**",
            description=f"{len(messages)} messages were deleted!",
            colour=discord.Colour.dark_red(),
        )
        embed.set_author(
            name=f"{str(self.bot.user)} ({self.bot.user.id})",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.timestamp = discord.utils.utcnow()

        # creates the file with the deleted messages
        message_list = []
        for message in messages:
            message_list.append(
                f"{str(message.author)} said at {message.created_at.replace(microsecond=0)} UTC: \n{message.content}\n\n"
            )
        buffer = StringIO("".join(message_list))
        f = discord.File(buffer, filename="deleted_messages.txt")

        logs = self.bot.get_channel(self.get_logchannel(messages[0].guild.id))

        # the file could theoratically be too large to send, the limit is 8MB.
        # realistically we will never, ever hit this
        try:
            await logs.send(embed=embed, file=f)
        except:
            await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(
            title="**🚫 New ban! 🚫**",
            description=f"{user.mention} has been banned from this server!",
            colour=discord.Colour.dark_red(),
        )
        embed.set_author(
            name=f"{str(user)} ({user.id})", icon_url=user.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(guild.id))
        await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(
            title="**🔓 New unban! 🔓**",
            description=f"{user.mention} has been unbanned from this server!",
            colour=discord.Colour.green(),
        )
        embed.set_author(
            name=f"{str(user)} ({user.id})", icon_url=user.display_avatar.url
        )
        embed.timestamp = discord.utils.utcnow()
        logs = self.bot.get_channel(self.get_logchannel(guild.id))
        await logs.send(embed=embed)


def setup(bot):
    bot.add_cog(Logging(bot))
    print("Logging cog loaded")
