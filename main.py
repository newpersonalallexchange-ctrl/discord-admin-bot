import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="%",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    print("Bot is ready!")


@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    if amount < 1 or amount > 100:
        return await ctx.send("❌ Amount must be between 1 and 100.")

    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 Deleted {amount} messages.")
    await msg.delete(delay=3)


@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=False
    )
    await ctx.send("🔒 Channel locked.")


@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(
        ctx.guild.default_role,
        send_messages=None
    )
    await ctx.send("🔓 Channel unlocked.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} has been kicked.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} has been banned.")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int = 10):
    if minutes < 1 or minutes > 40320:
        return await ctx.send("❌ Minutes must be between 1 and 40320.")

    duration = discord.utils.utcnow() + discord.utils.timedelta(
        minutes=minutes
    )

    await member.timeout(duration, reason=f"Timeout by {ctx.author}")
    await ctx.send(
        f"⏱️ {member.mention} timed out for {minutes} minutes."
    )


@bot.command()
async def server(ctx):
    guild = ctx.guild

    embed = discord.Embed(title=f"📊 {guild.name}")
    embed.add_field(name="Server ID", value=str(guild.id))
    embed.add_field(name="Members", value=str(guild.member_count))
    embed.add_field(name="Channels", value=str(len(guild.channels)))
    embed.add_field(name="Roles", value=str(len(guild.roles)))

    await ctx.send(embed=embed)


@bot.command()
async def av(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title=f"🖼️ {member.display_name}'s Avatar"
    )
    embed.set_image(url=member.display_avatar.url)

    await ctx.send(embed=embed)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.
