import discord


def read_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()


client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$pelado'):
        await message.channel.send('Ese fedeo toda la noche junto con pancho_toni')

client.run(read_token())

