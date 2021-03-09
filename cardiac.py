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
        text = message.content
        texts = [text]
        print(texts)
        print(Cardiac.predict(texts))
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user.name}")

    def find_word(w):
        return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search

    def get_profane_prob(prob):
        return prob[1]

    def predict(message):
        return Cardiac.model.predict(Cardiac.vectorizer.transform(message))

    def predict_prob(message):
        return np.apply_along_axis(Cardiac.get_profane_prob, 1, Cardiac.model.predict_proba(Cardiac.vectorizer.transform(message)))

    def main():
        Cardiac.model = joblib.load("model.joblib")
        Cardiac.vectorizer = joblib.load("vectorizer.joblib")
        bot.run(TOKEN)


if __name__ == "__main__":
    Cardiac.main()