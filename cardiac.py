import os
import re
import json
import discord
from discord.ext import commands


TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="+", intents=intents)


class Cardiac:
    filter = None

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

        content = message.content
        for word in Cardiac.filter:
            if Cardiac.find_word(word)(content):
                await message.channel.send("BANNED")
                break
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")
        print(Cardiac.filter)

    def find_word(w):
        return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search

    def main():
        with open("list.json") as f:
            data = json.load(f)
            Cardiac.filter = data["wordList"]
        bot.run(TOKEN)


if __name__ == "__main__":
    Cardiac.main()