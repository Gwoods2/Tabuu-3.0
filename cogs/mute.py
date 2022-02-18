import discord
from discord.ext import commands
import aiosqlite
import asyncio
from utils.ids import GuildNames, GuildIDs, TGRoleIDs, BGRoleIDs, AdminVars
from utils.time import convert_time
import utils.logger


class Mute(commands.Cog):
    """
    Contains the custom mute system for both of our servers.
    """

    def __init__(self, bot):
        self.bot = bot

    async def add_mute(self, guild: discord.Guild, member: discord.Member):
        """
        Adds the mute entry in the database,
        and tries to add the role in both servers.
        """
        # checks if the user is already flagged as muted in the file
        # if not, goes ahead and adds the mute.
        # no reason to have someone in there multiple times
        async with aiosqlite.connect("./db/database.db") as db:
            matching_user = await db.execute_fetchall(
                """SELECT * FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

            if len(matching_user) == 0:
                await db.execute(
                    """INSERT INTO muted VALUES (:user_id, :muted)""",
                    {"user_id": member.id, "muted": True},
                )

                await db.commit()

        # first we add the mute on the tg server, or try to
        try:
            tg_guild = self.bot.get_guild(GuildIDs.TRAINING_GROUNDS)
            tg_role = discord.utils.get(tg_guild.roles, id=TGRoleIDs.MUTED_ROLE)
            tg_member = tg_guild.get_member(member.id)
            await tg_member.add_roles(tg_role)
        except Exception as exc:
            logger = utils.logger.get_logger("bot.mute")
            logger.warning(
                f"Tried to add muted role in {GuildNames.TG} server but it failed: {exc}"
            )

        # then we add the mute on the bg server, or try to
        try:
            bg_guild = self.bot.get_guild(GuildIDs.BATTLEGROUNDS)
            bg_role = discord.utils.get(bg_guild.roles, id=BGRoleIDs.MUTED_ROLE)
            bg_member = bg_guild.get_member(member.id)
            await bg_member.add_roles(bg_role)
        except Exception as exc:
            logger = utils.logger.get_logger("bot.mute")
            logger.warning(
                f"Tried to add muted role in {GuildNames.BG} server but it failed: {exc}"
            )

    async def remove_mute(self, guild: discord.Guild, member: discord.Member):
        """
        Basically reverses the add_mute function.
        Removes the muted entry from the database
        and tries to remove the role in both servers.
        """
        async with aiosqlite.connect("./db/database.db") as db:
            await db.execute(
                """DELETE FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

            await db.commit()

        try:
            tg_guild = self.bot.get_guild(GuildIDs.TRAINING_GROUNDS)
            tg_role = discord.utils.get(tg_guild.roles, id=TGRoleIDs.MUTED_ROLE)
            tg_member = tg_guild.get_member(member.id)
            await tg_member.remove_roles(tg_role)
        except Exception as exc:
            logger = utils.logger.get_logger("bot.mute")
            logger.warning(
                f"Tried to remove muted role in {GuildNames.TG} server but it failed: {exc}"
            )

        try:
            bg_guild = self.bot.get_guild(GuildIDs.BATTLEGROUNDS)
            bg_role = discord.utils.get(bg_guild.roles, id=BGRoleIDs.MUTED_ROLE)
            bg_member = bg_guild.get_member(member.id)
            await bg_member.remove_roles(bg_role)
        except Exception as exc:
            logger = utils.logger.get_logger("bot.mute")
            logger.warning(
                f"Tried to remove muted role in {GuildNames.BG} server but it failed: {exc}"
            )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason):
        """
        Mutes a member in both servers indefinitely and DMs them the reason for it.
        """
        async with aiosqlite.connect("./db/database.db") as db:
            matching_user = await db.execute_fetchall(
                """SELECT * FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

        # we check again if the user is muted here because i dont want the user to get dm'd again if he already is muted
        # didn't wanna put a separate dm function as well because the dm's change depending on what command calls it
        if len(matching_user) == 0:
            await self.add_mute(ctx.guild, member)
            await ctx.send(f"{member.mention} was muted!")
            try:
                await member.send(
                    f"You have been muted in the {ctx.guild.name} Server for the following reason: \n```{reason}```\nIf you would like to discuss your punishment, please contact {AdminVars.GROUNDS_GENERALS}."
                )
            except Exception as exc:
                logger = utils.logger.get_logger("bot.mute")
                logger.warning(
                    f"Tried to message mute reason to {str(member)}, but it failed: {exc}"
                )

        else:
            await ctx.send("This user was already muted!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        """
        Unmutes a member in both servers and notifies them via DM.
        """
        async with aiosqlite.connect("./db/database.db") as db:
            matching_user = await db.execute_fetchall(
                """SELECT * FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

        if len(matching_user) != 0:
            await self.remove_mute(ctx.guild, member)
            await ctx.send(f"{member.mention} was unmuted!")
            try:
                await member.send(
                    f"You have been unmuted in the {ctx.guild.name} Server! Don't break the rules again"
                )
            except Exception as exc:
                logger = utils.logger.get_logger("bot.mute")
                logger.warning(
                    f"Tried to message unmute message to {str(member)}, but it failed: {exc}"
                )
        else:
            await ctx.send("This user was not muted!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tempmute(self, ctx, member: discord.Member, mute_time, *, reason):
        """
        Mutes a member in both servers, waits the specified time and unmutes them again.
        """
        # this here uses the convert_time function from my reminder to convert the input into the seconds, and also a human-readable-string
        seconds, time_muted = convert_time(mute_time)

        # just checking the duration is not at a crazy high/low value
        if seconds < 30:
            await ctx.send("Duration is too short! Minimum duration is 30 seconds.")
            return

        if seconds > 86401:
            await ctx.send("Duration is too long! Maximum duration is 1 day.")
            return

        # now this is basically just "%mute, wait specified time, %unmute" but automated into one command
        async with aiosqlite.connect("./db/database.db") as db:
            matching_user = await db.execute_fetchall(
                """SELECT * FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

        # the mute block from %mute, with the inclusion of time_muted
        if len(matching_user) == 0:
            await self.add_mute(ctx.guild, member)
            await ctx.send(f"{member.mention} was muted for *{time_muted}*!")
            try:
                await member.send(
                    f"You have been muted in the {ctx.guild.name} Server for ***{time_muted}*** for the following reason: \n```{reason}```\nIf you would like to discuss your punishment, please contact {AdminVars.GROUNDS_GENERALS}."
                )
            except Exception as exc:
                logger = utils.logger.get_logger("bot.mute")
                logger.warning(
                    f"Tried to message temp mute reason to {str(member)}, but it failed: {exc}"
                )

        else:
            await ctx.send("This user is already muted!")
            return

        # waits the specified time
        await asyncio.sleep(seconds)

        # need to refresh the contents of the database
        async with aiosqlite.connect("./db/database.db") as db:
            matching_user = await db.execute_fetchall(
                """SELECT * FROM muted WHERE user_id = :user_id""",
                {"user_id": member.id},
            )

        # the unmute block from %unmute, no need for another unmute confirmation if the user was unmuted before manually
        if len(matching_user) != 0:
            await self.remove_mute(ctx.guild, member)
            await ctx.send(f"{member.mention} was automatically unmuted!")
            try:
                await member.send(
                    f"You have been automatically unmuted in the {ctx.guild.name} Server! Don't break the rules again"
                )
            except Exception as exc:
                logger = utils.logger.get_logger("bot.mute")
                logger.warning(
                    f"Tried to message temp unmute message to {str(member)}, but it failed: {exc}"
                )

    # error handling for the mute commands
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify a reason for the mute!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Nice try, but you don't have the permissions to do that!")
        else:
            raise error

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to mention a member!")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Nice try, but you don't have the permissions to do that!")
        else:
            raise error

    @tempmute.error
    async def tempmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "You need to mention a member, an amount of time, and a reason!"
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("You need to mention a member!")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Nice try, but you don't have the permissions to do that!")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                "Invalid time format! Please use a number followed by d/h/m/s for days/hours/minutes/seconds."
            )
        else:
            raise error


def setup(bot):
    bot.add_cog(Mute(bot))
    print("Mute cog loaded")
