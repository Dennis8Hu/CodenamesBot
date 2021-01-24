#############################################
#   CodeNameBot V1.0 created by Dennis Hu   #
#   Thanks to Jorik Diks for emoji2txt      #
#   Github: Dennis8hu & Jorikdx             #
#   documentation on dennishu.net           #
#############################################

import discord
from discord.ext import commands
import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import math

TOKEN = ' '
prefix = '$'
intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
plt.style.use(['dark_background'])

global gamestarted, teamturn, roleturn, hintnumber, server, teamscores, listinuse, guessedlist, gamewords, teamcolor


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')


def text_to_emoji(text: str):
    textToEmojiDictionairy = {
        "A": ":regional_indicator_a:",
        "B": ":regional_indicator_b:",
        "C": ":regional_indicator_c:",
        "D": ":regional_indicator_d:",
        "E": ":regional_indicator_e:",
        "F": ":regional_indicator_f:",
        "G": ":regional_indicator_g:",
        "H": ":regional_indicator_h:",
        "I": ":regional_indicator_i:",
        "J": ":regional_indicator_j:",
        "K": ":regional_indicator_k:",
        "L": ":regional_indicator_l:",
        "M": ":regional_indicator_m:",
        "N": ":regional_indicator_n:",
        "O": ":regional_indicator_o:",
        "P": ":regional_indicator_p:",
        "Q": ":regional_indicator_q:",
        "R": ":regional_indicator_r:",
        "S": ":regional_indicator_s:",
        "T": ":regional_indicator_t:",
        "U": ":regional_indicator_u:",
        "V": ":regional_indicator_v:",
        "W": ":regional_indicator_w:",
        "X": ":regional_indicator_x:",
        "Y": ":regional_indicator_y:",
        "Z": ":regional_indicator_z:",
        " ": " ",
        "!": ":grey_exclamation:",
        "?": ":grey_question:",
        "0": ":zero:",
        "1": ":one:",
        "2": ":two:",
        "3": ":three:",
        "4": ":four:",
        "5": ":five:",
        "6": ":six:",
        "7": ":seven:",
        "8": ":eight:",
        "9": ":nine:",
        "#": ":hash:",
        "*": ":asterisk:"
    }
    emojiText = ""
    for i in range(0, len(text)):
        if text[i].upper() in textToEmojiDictionairy:
            emojiText += "" + textToEmojiDictionairy[text[i].upper()]

    return emojiText


def list_to_table(list: list, col: int):
    table = []
    lengthoflist = len(list)
    columns = math.floor(lengthoflist / col)
    lastbit = lengthoflist % col
    for i in range(columns):
        table += [list[0 + col * i:col-1 + col * i]]
    if lastbit:
        table += [list[col * columns:col * columns + lastbit]]
    table = f'```{tabulate(table)}```'
    return table


def color_format_table(namelist, color: str):
    if color == 'red':
        colorprefix = '- '
    elif color == 'green':
        colorprefix = '! '
    else:
        colorprefix = ''
    printstring = ''
    linesstring = tabulate([namelist]).split('\n')
    for i in range(len(linesstring)):
        linesstring[i] = colorprefix + linesstring[i] + '\n'
        printstring += linesstring[i]
    return printstring


def send_cards(index):
    global gamewords, roleturn, gamestarted, server, teamcolor, teamturn
    with open('CodenamesGame.txt', 'r') as f:
        teams = eval(str(f.read()))

    gamewords[index]['operativecolor'] = gamewords[index]['mastercolor'] #card gets turned

    fig2, ax = plt.subplots(figsize=(12, 6))
    for i in range(5):
        for j in range(5):
            ax.text((1 + i), (1 + j), str(gamewords[i * 5 + j]['index']) + ' ' + gamewords[i * 5 + j]['word'],
                    color=gamewords[i * 5 + j]['text'], ha='center', bbox=dict(facecolor=gamewords[i * 5 + j]['background'],
                    edgecolor=gamewords[i * 5 + j]['operativecolor'], boxstyle='round,pad=1'))

    plt.xlim([1, 5])
    plt.ylim([1, 5])
    plt.axis('off')
    plt.savefig("CNoperativePlot.png")

    if gamestarted and roleturn == 'operative': #meaning team chose the right card
        message = ' '
    elif gamestarted and roleturn == 'master': #meaning team chose the wrong card
        message = 'Waiting for hint...'
    else:
        message = f'Game won by {teamturn} team'

    embed = discord.Embed(title='CodeNames', description='\u200b', color=teamcolor[str(teamturn)])
    file = discord.File("CNoperativePlot.png", filename="image.png")  # filename should STAY image.png
    embed.set_image(url="attachment://image.png")
    embed.add_field(name=f"Red: {teamscores['red']}", value='\u200b list of hints', inline=True)  # u200b = whitespace
    embed.add_field(name=f"Blue: {teamscores['blue']}", value='\u200b list of hints', inline=True)
    embed.add_field(name='\u200b', value=f'{teamturn} turn\n{message}', inline=False)
    return embed, file


@client.command()
async def CN(ctx, command: str = None):
    if command == 'list':
        await ctx.send('$CNlist creates new lists or appends words to a existing list.\n'
                 'Use "$CNlist [list title][new words separated by one space]"')
    elif command == 'listshow':
        await ctx.send('$CNlistshow shows the existing lists by title.\n'
                 'Use "$CNlistshow" to show the list of existing word list titles.\n'
                 'Use "$CNlistshow [list title]" to show the words within the list')
    elif command == 'new':
        await ctx.send('$CNnew creates a new game. This refreshes the player team list')
    elif command == 'join':
        await ctx.send('$CNjoin allows players to choose a team and position.\n'
                 'Use "$CNjoin [red/blue] [master\operative]" to join a team.\n'
                 'Feature to be added: random teams each round')
    elif command == 'start':
        await ctx.send('$CNstart starts a game.\n'
                 'Feature to be added: random team starts')
    elif command == 'hint':
        await ctx.send('$CNhint allows masters of the team to send in a hint.\n'
                 'Use "$CNhint [hint] [integer]" send the hint')
    elif command == 'guess':
        await ctx.send('$CNguess allows operatives to guess a card.\n'
                 'Use "$CNguess [integer]" to guess the card that is not yet identified')

    else:
        listofcommands = ['list', 'listshow', 'new', 'join', 'start', 'hint', 'guess']
        await ctx.send(f'Type:\n '
                       f'$CN [{listofcommands}]\n'
                       f'for more info on that command')


@client.command()
async def CNlist(ctx, listname: str, *newwordlist):
    with open('CodenamesList.txt', 'r') as f:
        wordlist = eval(str(f.read()))

    if listname in wordlist:
        wordlist[listname] += list(newwordlist)
    else:
        wordlist[listname] = list(newwordlist)

    await ctx.send(f'New list {listname}: {wordlist[listname]}')

    with open('CodenamesList.txt', 'w') as f:
        f.write(str(wordlist))


@client.command()
async def CNlistshow(ctx, listname: str = None):
    with open('CodenamesList.txt', 'r') as f:
        wordlist = eval(str(f.read()))
    if listname:
        table = list_to_table(wordlist[listname], 8)
        await ctx.send(table)
        await ctx.send(f'List: {listname}, words: {len(wordlist[listname])}')
    else:
        await ctx.send(tabulate([wordlist.keys()]))


@client.command()
async def CNnew(ctx):
    ### Make games guild dependent ###
    players = []
    global server
    server = ctx
    guild = ctx.guild
    if guild:
        with open('CodenamesGame.txt', 'w') as f:
            f.write(str(players))
        await ctx.send(f"New game is started on {ctx.guild}. Type '{prefix}CNjoin [red/blue] [master/operative]' to join.")
    else:
        await ctx.send('Cannot create a new game outside a guild.')


@client.command()
async def CNjoin(ctx, team: str, role: str):
    with open('CodenamesGame.txt', 'r') as f:
        teams = eval(str(f.read()))

    redteam = []
    blueteam = []

    PlayerName = ctx.author.name
    PlayerID = ctx.author.id
    if (team == 'blue' or team == 'red') and (role == 'master' or role == 'operative'):
        teams.append({'ID': str(PlayerID), 'team': team, 'role': role, 'name': PlayerName})

        for player in teams:
            if player['team'] == 'red' and player['role'] == 'master':
                redteam += [f'master: {player["name"]}']
            elif player['team'] == 'red' and player['role'] == 'operative':
                redteam += [f'operative: {player["name"]}']
            elif player['team'] == 'blue' and player['role'] == 'master':
                blueteam += [f'master: {player["name"]}']
            elif player['team'] == 'blue' and player['role'] == 'operative':
                blueteam += [f'operative: {player["name"]}']

        await ctx.send(f'```diff\n{color_format_table(redteam, "red")}\n```')
        await ctx.send(f'```diff\n{color_format_table(blueteam, "green")}\n```')

        with open('CodenamesGame.txt', 'w') as f:
            f.write(str(teams))
    else:
        if team != 'blue' and team != 'red': await ctx.send(f'Bruh, {team} is not a team')
        if role != 'master' and role != 'operative': await ctx.send(f'Bruh, {role} is not a role')

    user = client.get_user(PlayerID)
    await user.send('👀')


@client.command()
async def CNstart(ctx, listname: str = 'numbers'):
    with open('CodenamesGame.txt', 'r') as f:
        teams = eval(str(f.read()))
    with open('CodenamesList.txt', 'r') as f:
        wordlist = eval(str(f.read()))
        wordlist = wordlist[listname]

    global teamscores, gamestarted, teamturn, roleturn, server, listinuse, guessedlist, gamewords, teamcolor
    teamscores = {'red': 9, 'blue': 8}
    gamestarted = True
    teamturn = 'red'
    teamcolor = {'red': 0xff0000, 'blue': 0x0037ff}
    roleturn = 'master'
    server = ctx
    guild = ctx.guild
    listinuse = listname
    guessedlist = []

    if guild:
        # Generate the playing cards
        random.shuffle(wordlist)

        for i in range(len(wordlist)):
            if i < 8:
                wordlist[i] = {'mastercolor': 'red', 'word': wordlist[i], 'text': 'black'}
            if 7 < i < 17:
                wordlist[i] = {'mastercolor': 'blue', 'word': wordlist[i], 'text': 'black'}
            if i == 17:
                wordlist[i] = {'mastercolor': 'white', 'word': wordlist[i], 'text': 'white'}
            if 17 < i < 26:
                wordlist[i] = {'mastercolor': 'grey', 'word': wordlist[i], 'text': 'grey'}
        del wordlist[26: len(wordlist)]
        random.shuffle(wordlist)

        for i in range(len(wordlist)):
            wordlist[i]['index'] = i
            wordlist[i]['operativecolor'] = 'white'
            wordlist[i]['font'] = 'white'
            wordlist[i]['background'] = 'none'

        gamewords = wordlist
        fig1, ax = plt.subplots(figsize=(12, 6))
        for i in range(5):
            for j in range(5):
                ax.text((1 + i), (1 + j), str(wordlist[i*5 + j]['index']) + ' ' + wordlist[i*5 + j]['word'],
                    color=wordlist[i*5+j]['mastercolor'], ha='center', bbox=dict(facecolor='none',
                    edgecolor=wordlist[i*5+j]['mastercolor'], boxstyle='round,pad=1'))
        plt.xlim([1, 5])
        plt.ylim([1, 5])
        plt.axis('off')
        plt.savefig("CNMasterPlot.png")

        plt.clf()
        plt.close('all')

        fig2, ax = plt.subplots(figsize=(12, 6))
        for i in range(5):
            for j in range(5):
                ax.text((1 + i), (1 + j), str(wordlist[i*5 + j]['index']) + ' ' + wordlist[i*5 + j]['word'],
                    color=wordlist[i*5+j]['operativecolor'], ha='center', bbox=dict(facecolor='none',
                    edgecolor=wordlist[i*5+j]['operativecolor'], boxstyle='round,pad=1'))
        plt.xlim([1, 5])
        plt.ylim([1, 5])
        plt.axis('off')
        plt.savefig("CNoperativePlot.png")

        for player in teams:
            if player['role'] == 'master':
                user = client.get_user(int(player['ID']))
                await user.send(file=discord.File('CNMasterPlot.png'))

        embed = discord.Embed(title='CodeNames', description='\u200b', color=teamcolor[teamturn])
        file = discord.File("CNoperativePlot.png", filename="image.png") #filename should STAY image.png
        embed.set_image(url="attachment://image.png")
        embed.add_field(name=f"Red: {teamscores['red']}", value='\u200b', inline=True) #u200b = whitespace
        embed.add_field(name=f"Blue: {teamscores['blue']}", value='\u200b', inline=True)
        embed.add_field(name='\u200b', value=f'{teamturn} turn\n waiting for hint...', inline=False)
        await ctx.send(embed=embed, file=file)

    else: await ctx.send('Cannot start a game outside a guild.')


@client.command()
async def CNhint(ctx, hint: str, hintwordamount: int):
    with open('CodenamesGame.txt', 'r') as f:
        players = eval(str(f.read()))

    global hintnumber, roleturn

    if gamestarted:
        playercert = next(item for item in players if item['ID'] == str(ctx.author.id))
        if playercert['role'] == 'master' and playercert['team'] == teamturn:
            hintnumber = hintwordamount
            await server.send(f'Hint for {teamturn} team:')
            await server.send(f'{text_to_emoji(hint)}\t {text_to_emoji(str(hintwordamount))}') #Make all the previoos hints visible on embed
            roleturn = 'operative'
        else: await ctx.send('Hey peasant, know your place >:(.')
    else:
        await ctx.send('Currently no game is running')


@client.command()
async def CNguess(ctx, guess: int):
    with open('CodenamesGame.txt', 'r') as f:
        players = eval(str(f.read()))

    global gamestarted, teamturn, roleturn, guessedlist, teamscores, gamewords

    teaminverse = 'blue' if teamturn == 'red' else 'blue'

    playercert = next(item for item in players if item['ID'] == str(ctx.author.id))

    if guess in guessedlist:
        await ctx.send(f'{guess} is not an option boi.')
    else:
        if gamestarted:
            if playercert['role'] == 'operative' == roleturn and playercert['team'] == teamturn:
                guessedlist.append(int(guess))

                if gamewords[guess]['mastercolor'] == teamturn:
                    teamscores[teamturn] -= 1
                    gamewords[guess]['operativecolor'] = teamturn
                    gamewords[guess]['background'] = teamturn
                    gamewords[guess]['text'] = 'white'
                    print('chose the correct one')

                elif gamewords[guess]['mastercolor'] == teaminverse:
                    teamscores[teaminverse] -= 1
                    gamewords[guess]['operativecolor'] = teaminverse
                    gamewords[guess]['background'] = teaminverse
                    gamewords[guess]['text'] = 'white'
                    teamturn = teaminverse
                    roleturn = 'master'
                    print('chose the incorrect one')

                elif gamewords[guess]['mastercolor'] == 'grey':
                    gamewords[guess]['operativecolor'] = 'grey'
                    gamewords[guess]['background'] = 'grey'
                    gamewords[guess]['text'] = 'white'
                    teamturn = teaminverse
                    print('chose the grey one')

                elif gamewords[guess]['mastercolor'] == 'white':
                    gamewords[guess]['operativecolor'] = 'black'
                    gamewords[guess]['background'] = 'white'
                    gamewords[guess]['text'] = 'black'
                    gamestarted = False
                    teamturn = teaminverse
                    print('chose the worst one')

                await server.send(embed=send_cards(guess)[0], file=send_cards(guess)[1])

                if teamscores['red'] == 0 or teamscores['blue'] == 0 or gamestarted == False:
                    await ctx.send(text_to_emoji(f'{teamturn} team won!'))

            else: await ctx.send(f"Hey you're not your turn {playercert['team']} {playercert['role']}, know your place >:(.")
        else:
            await ctx.send('Currently no game is running')


client.run(TOKEN)
