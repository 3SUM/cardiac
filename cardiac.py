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
    async def on_guild_join(self, guild):
        print(f"{bot.user.name} joined {guild.name}")

    @bot.event
    async def on_member_join(self, member):
        print(f"{member.name} has joined!")

    @bot.event
    async def on_member_remove(self, member):
        print(f"{member.name} has left!")

    @bot.event
    async def on_message(self, message):
        if message.author == bot.user:
            return

        guild = message.guild
        member = message.author
        content = message.content
        for word in self.filter:
            if self.find_word(word)(content):
                await message.delete()
                await guild.ban(member, reason="Used profanity")
                banned_embed = discord.Embed(
                    title="Banned User",
                    description=f"{member.name} has been banned!",
                    color=0xE73C24,
                )
                await message.channel.send(embed=banned_embed)
                break
        await bot.process_commands(message)

    @bot.event
    async def on_ready(self):
        print(f"Logged in as {bot.user.name}")

    def find_word(self, w):
        return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search

    def main(self):
        with open("list.json") as f:
            data = json.load(f)
            self.filter = data["wordList"]
        bot.run(TOKEN)


if __name__ == "__main__":
    cardiac = Cardiac()
    cardiac.main()