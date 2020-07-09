import discord

token = 'NzMwNjcwNTU4NjM4NzY4MTc4.Xwa4Eg.s_J17XYdlUtfslxx3D98XDuZJXo'
client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$pelado'):
        await message.channel.send('Ese fedeo toda la noche junto con pancho_toni')

client.run(token)

