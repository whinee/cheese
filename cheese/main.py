from os import environ as env

import discord

from settings import stg

STG = stg(None, "roles.yml")
CE_DICT = {}

for k, v in STG.items():
    CE_DICT[k] = {discord.PartialEmoji(name=vk): vv for vk, vv in v["kv"].items()}


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id not in CE_DICT:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return

        try:
            role_id = CE_DICT[payload.message_id][payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        try:
            await payload.member.add_roles(role)
        except discord.HTTPException:
            pass
        
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        if payload.message_id not in CE_DICT:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            return
        
        try:
            role_id = CE_DICT[payload.message_id][payload.emoji]
        except KeyError:
            return

        role = guild.get_role(role_id)
        if role is None:
            return

        try:
            await member.remove_roles(role)
        except discord.HTTPException:
            pass

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(env["BOT_TOKEN"])