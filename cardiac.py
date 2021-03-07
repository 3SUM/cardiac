import os
import discord
from discord.ext import commands


TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)


class Cardiac:
    @bot.event
    async def on_guild_join(guild):
        print(f"{bot.user.name} joined {guild.name}")

    @bot.event
    async def on_member_join(member):
        print(f"{member.name} has joined!")

    @bot.event
    async def on_member_remove(member):
        print(f"{member.name} has left!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    def main():
        bot.run(TOKEN)


if __name__ == "__main__":
    Cardiac.main()