import os
import re
import json
import discord
import joblib
import numpy as np
from discord.ext import commands


TOKEN = os.environ["TOKEN"]

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="+", intents=intents)


class Cardiac:
    model = None
    vectorizer = None

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

        guild = message.guild
        member = message.author
        warned_role = discord.utils.get(guild.roles, name="Warned")

        text = [message.content]
        prob = Cardiac.predict_prob(text)
        if prob >= 0.80:
            print(f"{message.content} [{prob}]")
            if warned_role in member.roles:
                await message.delete()
                await guild.ban(member, reason="Used profanity")
                banned_embed = discord.Embed(
                    title="Banned User",
                    description=f"{member.name} has been banned!",
                    color=0xE73C24,
                )
                await message.channel.send(embed=banned_embed)
            else:
                await message.delete()
                await discord.Member.add_roles(member, warned_role)
                warned_embed = discord.Embed(
                    title="Warned User",
                    description=f"{member.mention} has been warned!",
                    color=0xE73C24,
                )
                await message.channel.send(embed=warned_embed)
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    def get_profane_prob(prob):
        return prob[1]

    def predict(message):
        return Cardiac.model.predict(Cardiac.vectorizer.transform(message))

    def predict_prob(message):
        return np.apply_along_axis(
            Cardiac.get_profane_prob,
            1,
            Cardiac.model.predict_proba(Cardiac.vectorizer.transform(message)),
        )

    def main():
        Cardiac.model = joblib.load("data/model.joblib")
        Cardiac.vectorizer = joblib.load("data/vectorizer.joblib")
        bot.run(TOKEN)


if __name__ == "__main__":
    Cardiac.main()