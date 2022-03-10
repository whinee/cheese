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
        
    async def on_ready(self):
        for k, v in STG.items():
            ci = v["md"]["chnl"]
            channel = await self.fetch_channel(ci)
            message = await channel.fetch_message(k)
            for r in message.reactions:
                try:
                    role_id = v["kv"][r.emoji]
                except KeyError:
                    pass

                guild = message.guild
                role = guild.get_role(role_id)
                if role is None:
                    pass
                users = await r.users().flatten()
                for u in users:
                    try:
                        u = await guild.fetch_member(u.id)
                        await u.add_roles(role)
                    except discord.HTTPException:
                        pass
        await self.logout()

intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run(env["BOT_TOKEN"])