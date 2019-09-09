import discord
import requests
from setting import BOT_TOKEN
from discord.ext.commands import Bot
from bs4 import BeautifulSoup


bot = Bot(command_prefix=('!', '?'))

@bot.command(pass_context=True, aliases=['fp', 'find', 'stats'])
async def findProfile(ctx, arg):
    URL = 'https://lolchess.gg/profile/na/'+arg
    headers = {"User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    stats = []
    try:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        profile_summary = soup.find("div", class_="profile__tier")
        profile_stats = profile_summary.find_all(text=True, recursive=True)

        summoner_icon = soup.find("div", class_="profile__icon").img['src']
        summoner_icon = 'https:' + summoner_icon

        rank_icon = 'https:' + profile_summary.find("img")['src']

        for data in profile_stats:
            if data == '\n':
                continue
            stats.append(data.strip())
        tier_rank = stats[1]
        lp = stats[2]
        games_played = stats[6]
        games_won = stats[12]
        games_lost = stats[15]
        win_rate = stats[9]

        embed = discord.Embed(
            title='TFT Profile',
            url=URL,
            color=discord.Color.blue()

        )
        embed.set_image(url=rank_icon)
        embed.set_thumbnail(url=summoner_icon)
        embed.set_author(name=arg)
        embed.add_field(name='Tier', value=tier_rank, inline=True)
        embed.add_field(name='LP', value=lp, inline=True)
        embed.add_field(name='Games Played', value=games_played, inline=True)
        embed.add_field(name='WinRate', value=win_rate, inline=True)
        embed.add_field(name='Games Won', value=games_won, inline=True)
        embed.add_field(name='Games Lost', value=games_lost, inline=True)

        await  ctx.send(embed=embed)

    except AttributeError as e:
        print(e)
        await ctx.send('Summoner Not Found')





bot.run(BOT_TOKEN)


