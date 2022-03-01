import discord
from discord.ext import commands
import re


class Bot(commands.Bot):
    async def on_ready(self):
        print("Logged on as", self.user)


bot = Bot(
    command_prefix=commands.when_mentioned_or("uwu: "),
    description="A quick bot for quoting posts fast enough cuz squish can't do it for his bot rn wehwoehgweghwgwe[oef",
)


def getIDFromChannelMention(channel_id_mention):
    return int(re.match("<#(\d+)>", channel_id_mention).group(1))


@bot.command()
async def quote(ctx, _from_channel, _to_channel, *message_ids):
    from_channel = discord.utils.get(ctx.guild.channels, id=getIDFromChannelMention(_from_channel))
    to_channel   = discord.utils.get(ctx.guild.channels, id=getIDFromChannelMention(_to_channel))

    await ctx.send(content = "from: " + from_channel.name + '\n' +
                   "to: " + to_channel.name + '\n')

    for message_id in message_ids:
        found_message = await from_channel.fetch_message(message_id)

        embed = discord.Embed(
            title="message link!",
            description=found_message.content,
            url=found_message.jump_url,
            color=discord.Color(0xAC9CFF)
        )

        embed.set_author(name=found_message.author.name, icon_url=found_message.author.avatar_url)
        embed.set_footer(text=f"{found_message.author} • {found_message.author.id}", icon_url=found_message.author.avatar_url)

        if len(found_message.attachments) == 1: # If only one attachment
            webhook = await createWebhook(to_channel)
            embed.set_image(url=found_message.attachments[0].url)
            await webhook.send(embed=embed)

        else: # I guess that's some twitter post or multiple attachments
            is_linked = len(found_message.attachments) == 0
            attachments = found_message.embeds if is_linked else found_message.attachments

            webhook = await createWebhook(to_channel)

            embeds: list[discord.Embed] = [embed]
            for i, _embed in enumerate(attachments[1:], start=2):
                sub_embed = discord.Embed(color=discord.Color(0xAC9CFF))
                sub_embed.set_image(url=_embed.image.url if is_linked else _embed.url)
                sub_embed.set_footer(
                    text=f"{i}/{len(attachments)} • {found_message.author} • {found_message.author.id}",
                    icon_url=found_message.author.avatar_url
                )
                embeds.append(sub_embed)

            embed.set_image(url=attachments[0].image.url if is_linked else attachments[0].url)
            embed.set_footer(
                text=f"{1}/{len(attachments)} • {found_message.author} • {found_message.author.id}",
                icon_url=found_message.author.avatar_url
            )
            await webhook.send(embeds=embeds)


async def createWebhook(channel: discord.TextChannel):
    webhook_name = "Rira Chan"
    webhooks: list[discord.Webhook] = await channel.webhooks()
    for webhook in webhooks:
        if webhook_name == webhook.name:
            return webhook

    with open("rira.png", "rb") as avy:
        new_webhook = await channel.create_webhook(
            name=webhook_name,
            avatar=avy.read(),
            reason="Temporary Webhook for copying messages to other channels made by Zly."
        )

    return new_webhook

with open("token.uwu", "r") as token:
    bot.run(token.read())