import discord
from fetcher import stats, show_help, refresh, get_nick, w_l, last, avg, total, wins_rank


def read_token():
    with open('token.txt', 'r') as f:
        return f.readline().strip()


client = discord.Client()

players = {'gonza': 324686074, 'seba': 179677205, 'gena': 134129467, 'pancho': 137703388, 'yair': 156552375,
           'pela': 130817647,
           'chino': 135179013, 'statham': 145875771, 'lucas': 275221784, 'snoop': 354096578, 'negro': 140411170}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello noob')

    if message.content.startswith('!stats') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(stats(players[message.content.split()[1]]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!help') or message.content.startswith('!commands'):
        await message.channel.send(show_help())

    if message.content.startswith('!refresh') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            refresh(players[message.content.split()[1]])
            await message.channel.send("Ok (aguanta 1 toque)")

    if message.content.startswith('!players'):
        string = ""
        for key in players:
            try:
                name = get_nick(players[key])
                string += key + " **(" + str(name) + ")**\n"
            except KeyError or TypeError:
                continue

        await message.channel.send(string)

    if message.content.startswith('!wl') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(w_l(players[message.content.split()[1]]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!last') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(last(players[message.content.split()[1]]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!avg') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(avg(players[message.content.split()[1]]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!total') and len(message.content.split()) > 1:
        if message.content.split()[1] not in players:
            await message.channel.send("Ni idea quien es ese. Tira !players para ver los que conozco")
        else:
            try:
                await message.channel.send(total(players[message.content.split()[1]]))
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!wins'):
        string = wins_rank(players)

        await message.channel.send(string)

client.run(read_token())
