import discord
import typing
from discord.ext import commands


class owner(commands.Cog, name="Owner"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="shutdown", aliases=["logout"])
    @commands.is_owner()
    async def jsk_shutdown(self, ctx: commands.Context):
        """
        Logs this bot out.
        """

        await ctx.send("Logging out now")
        await ctx.bot.logout()


    @commands.command(brief="unload a cog")
    @commands.is_owner()
    async def unload(self, ctx, *, cog):
        """
        Unloads A.K.A. disables the given cog
        """
        if cog == 'cogs.owner':
            await ctx.send('**You cannot unload the owner cog as this cog allows unloading/reloading/loading cogs.**')
            return
        try:
            self.bot.unload_extension(cog)
            await ctx.send(f'Successfully unloaded`{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to unload {cog}\n```py\n{e}\n```')


    @commands.command(brief="load a cog")
    @commands.is_owner()
    async def load(self, ctx, *, cog):
        """
        Loads A.K.A. enables the given cog
        """
        try:
            self.bot.load_extension(cog)
            await ctx.send(f'Successfully loaded `{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')


    @commands.command(brief="Reload a cog")
    @commands.is_owner()
    async def reload(self, ctx, *, cog):
        """
        Reloads A.K.A. restarts the given cog
        """
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f'Successfully reloaded `{cog}`.')
        except Exception as e:
            await ctx.send(f'Failed to load {cog}\n```py\n{e}\n```')


    @commands.group(brief="Change bot appearance")
    @commands.is_owner()
    async def change(self, ctx):
        """
        Group command for status changing
        """
        if ctx.invoked_subcommand is None:
            pass


    @change.command(brief="Change playing status")
    @commands.is_owner()
    async def playing(self, ctx, *, playing: str):
        """
        Change the bot's playing status
        """
        try:
            await self.bot.change_presence(
                activity=discord.Game(type=0, name=playing),
                status=discord.Status.online
            )
            await ctx.send(f"Successfully changed Playing status to:\n{playing}")
            await ctx.message.delete()
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(e)


    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, id):
        guild = self.bot.fetch_guild(id)
        await ctx.send(guild.name)
        


    @commands.group(name='blacklist', invoke_without_command=True, enabled=True)  # invoke_without_command means you can have separate permissions/cooldowns for each subcommand
    @commands.is_owner()
    async def blacklist(self, ctx):
        """
        Group command for blacklisting
        """
        await ctx.send_help(ctx.command)


    @blacklist.command(name='user', enabled=True)
    @commands.is_owner()
    async def blacklist_user(self, ctx, user: typing.Union[discord.User, int], *, reason: str):
        """
        Blacklist or unblacklist a user
        """
        try:
            if isinstance(user, discord.User):
                print('pass discord.User')
                user = user
            elif isinstance(user, int):
                user = await self.bot.fetch_user(user)
            print('fetch user')
        except Exception as e:
            await ctx.send(f"Failed to find the user: `{e}`")
            print('caught exception')
        
        try:
            self.bot.blacklist[user.id]
            self.bot.database.execute(f"DELETE FROM blacklist WHERE id = {user.id}")
            self.bot.blacklist.pop(user.id)
            await ctx.send(f"unblacklisted {user}")
            print('unblacklisted')
        except Exception:
            self.bot.database.execute(f"INSERT INTO blacklist(id, reason) VALUES({user.id}, {reason})")
            self.bot.blacklist[user.id] = reason
            await ctx.send(f"blacklisted {user}")
            print('blacklisted')


    @blacklist.command(name='server', enabled=True)
    @commands.is_owner()
    async def blacklist_server(self, ctx, server: int, *, reason: str):
        """
        Blacklist or unblacklist a server
        """
        if not self.bot.get_guild(server):
            return await ctx.send("That server was not found make sure the ID is correct or if I'm in the server.")
        try:
            self.bot.blacklist[server]
            self.bot.database.execute(f"DELETE FROM blacklist WHERE id = {server}")
            self.bot.blacklist.pop(server)
            await ctx.send(f"unblacklisted {server}")          
        except Exception:
            self.bot.database.execute(f"INSERT INTO blacklist(id, reason) VALUES({server}, {reason})")
            self.bot.blacklist[server] = reason
            await ctx.send(f"blacklisted {server}")

            
def setup(bot):
    bot.add_cog(owner(bot))
