import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")
DEFAULT_MESSAGE = os.getenv("DEFAULT_MESSAGE", "")

if not TOKEN:
    raise ValueError("Missing TOKEN in Railway Variables")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print(f"Prefix: {PREFIX}")

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Bot Commands",
        description=f"Prefix: `{PREFIX}`",
        color=discord.Color.blue()
    )
    embed.add_field(name=f"{PREFIX}dm @user message", value="Send DM to one user only", inline=False)
    embed.add_field(name=f"{PREFIX}announce #channel message", value="Send announcement to a channel", inline=False)
    embed.add_field(name=f"{PREFIX}ping", value="Check bot latency", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

@bot.command(name="dm")
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, message=None):
    final_message = message or DEFAULT_MESSAGE

    if not final_message.strip():
        return await ctx.send("❌ No message provided.")

    if member.bot:
        return await ctx.send("❌ I can't DM bots.")

    try:
        await member.send(final_message)
        await ctx.send(f"✅ DM sent to {member.mention}")
    except Exception as e:
        await ctx.send(f"❌ Failed to DM user: `{e}`")

@bot.command(name="announce")
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: discord.TextChannel, *, message):
    embed = discord.Embed(
        description=message,
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Announced by {ctx.author}", icon_url=ctx.author.display_avatar.url)

    await channel.send(embed=embed)
    await ctx.send(f"✅ Announcement sent to {channel.mention}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🚫 You need administrator permission.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Missing: `{error.param.name}`")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        await ctx.send("❗ Error. Check Railway logs.")
        raise error

bot.run(TOKEN)
