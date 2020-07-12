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

                last_game = last(players[message.content.split()[1]])

                embed = discord.Embed(
                    colour=discord.Color.green() if last_game.get_wl().startswith(
                        ":green") else discord.Color.dark_red(),
                    title=last_game.get_title(),
                    description=last_game.get_wl())
                embed.set_author(name=last_game.get_hero_name(), icon_url=last_game.get_hero_icon())
                embed.add_field(name="KDA", value=last_game.get_kda())
                embed.add_field(name="Duracion", value=last_game.get_duracion())
                embed.add_field(name="Last Hits", value=last_game.get_lh())
                embed.add_field(name="OPM", value=last_game.get_opm())
                embed.add_field(name="EPM", value=last_game.get_epm())
                embed.add_field(name="Daño", value=last_game.get_dano())
                embed.add_field(name="Daño a torres", value=last_game.get_dano_t())
                embed.add_field(name="Curacion", value=last_game.get_curacion())
                embed.set_footer(text=last_game.get_time_ago())
                embed.set_thumbnail(url=last_game.get_hero_img())

                await message.channel.send(embed=embed)

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
                total_obj = total(players[message.content.split()[1]])
                embed = discord.Embed(title=total_obj.get_titulo(), colour=discord.Color.purple(),
                                      description="Contador de todas las partidas jugadas")
                embed.set_thumbnail(url=total_obj.get_thumbnail())

                embed.add_field(name="Kills", value=total_obj.get_kills())
                embed.add_field(name="Muertes", value=total_obj.get_muertes())
                embed.add_field(name="Assists", value=total_obj.get_assists())
                embed.add_field(name="Last Hits", value=total_obj.get_lh())
                embed.add_field(name="Denegados", value=total_obj.get_denegados())
                embed.add_field(name="Daño", value=total_obj.get_dano())
                embed.set_footer(text="Cortesia de sie7e-BOT", icon_url="https://steamcdn-a.akamaihd.net/apps/dota2/images/heroes/rattletrap_icon.png")

                await message.channel.send(embed=embed)
            except KeyError:
                await message.channel.send("Tiene el perfil privado esa caquita")

    if message.content.startswith('!wins'):
        string = wins_rank(players)

        await message.channel.send(string)


client.run(read_token())
