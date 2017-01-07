# NOQA
import random
import asyncio
from datetime import datetime, date
import requests
from discord.ext import commands

ORDMAX = date(2100, 12, 31).toordinal()


class General:
    """Commands that don't fit anywhere else."""

    def __init__(self, bot):
        """Cog constructor."""
        self.bot = bot
        asyncio.get_event_loop().call_soon(self._anime_auth)

    @commands.command(aliases=["choose"])
    async def choice(self, *choices: str):
        """Select one of the choices passed at random."""
        choice_list = " ".join(choices).split(";")
        choice_str = ""
        for cur in choice_list:
            choice_str += "`{}`, ".format(cur)

        await self.bot.reply("""is deciding between: {}

I choose: {}!""".format(choice_str, random.choice(choice_list)))

    @commands.command()
    async def eball(self, *ask: str):
        """Reply to question with an emoji."""
        the_e_list = [
            ":heart_eyes_cat:",
            ":revolving_hearts:",
            ":confounded:",
            ":expressionless:",
            ":smirk_cat:",
            ":no_entry_sign:",
            ":thumbsdown:",
            ":thumbsup:",
            ":ballot_box_with_check:",
            ":cool:",
            ":sweat_drops:",
            ":fire:",
            ":ok_hand:",
            ":middle_finger:"
        ]

        quote = "`{}`".format(" ".join(ask))

        await self.bot.reply("""{}\n{}""".format(
            quote, random.choice(the_e_list)
        ))

    @commands.command(name='8ball')
    async def eightball(self, *q: str):
        """Given a question, randomly answer it."""
        answers = [
            'It is certain.',
            'Of course.',
            ':crystal_ball: Perhaps...',
            'That\'s not a good idea.',
            'You\'ll just have to wait and see.',
            'Outlook good.',
            'Yes.',
            'No.',
            'Most likely ( ͡° ͜ʖ ͡°)',
            'Yes, definitely! (๑✧◡✧๑)',
            'Don\'t count on it (っ◞‸◟c)',
            'Not so sure... probably not.',
            'Not sure, but likely yes. :^)',
            'Without a doubt (^～^)',
            'That\'s completely absurd.',
            'No, absolutely not! :thumbsdown:',
            'I don\'t know m8 ʅ(◔౪◔ ) ʃ',
            ':crystal_ball: The answer is not what you think.',
            ':^)',
            ':^(',
            '>///<'
        ]
        await self.bot.reply('`{}`: {}'.format(' '.join(q),
                                               random.choice(answers)))

    @commands.command(name='8user',
                      brief='Given a question, randomly select a user.')
    async def eightuser(self, *q: str):
        """Given a question, randomly select a user.

        This is done by utilizing a neural network to analyze its intent
        and intelligently select the user that most completely fits the
        situation at hand.
        """
        user = random.choice(list(self.bot.get_all_members())).display_name
        await self.bot.reply('`{}`: {}'.format(' '.join(q), user))

    @commands.command(name='8usero')
    async def eightusero(self, *q: str):
        """Given a question, randomly select an online user."""
        member_list = list(self.bot.get_all_members())
        while True:
            user = random.choice(member_list)
            if user.status == user.status.online:
                break
        await self.bot.reply('`{}`: {}'.format(' '.join(q), user.display_name))

    @commands.command(name='8date')
    async def eightdate(self, *args: str):
        """Generate a random date."""
        ord_today = date.today().toordinal()
        arglist = "".join(args).split(" ")
        yearlist = []
        try:
            for year in arglist:
                yearlist.append(int(year))
        except TypeError:
            await self.bot.reply("Invalid arguments!?")
        if (len(arglist) == 0):
            await self.bot.reply(
                date.fromordinal(random.randint(ord_today, ORDMAX)))
        elif (len(arglist) == 1):
            ord_argmax = date.toordinal(date(yearlist[0], 12, 31))
            await self.bot.reply(
                date.fromordinal(random.randint(ord_today, ord_argmax)))
        elif len(arglist) == 2:
            ord_argmin = date.toordinal(date(yearlist[0], 1, 1))
            ord_argmax = date.toordinal(date(yearlist[1], 12, 31))
            await self.bot.reply(
                date.fromordinal(random.randint(ord_argmin, ord_argmax)))
        else:
            await self.bot.reply("Too many arguments!?")

    @commands.command()
    async def anime(self, *anime_name: str):
        """Get details about an anime."""
        query = ' '.join(anime_name)
        auth = {'access_token': self.anilist_auth['access_token']}
        results = requests.get('http://anilist.co/api/anime/search/' + query,
                               params=auth)
        if type(results.json()) is not list:
            await self.bot.say('Error: ' + ' '.join(
                results.json()['error']['messages']))
        else:
            id = str(results.json()[0]['id'])
            anime = requests.get('http://anilist.co/api/anime/' + id,
                                 params=auth)
            info = anime.json()
            if info['title_english'] != info['title_romaji']:
                name = '**{}** / {}'.format(info['title_romaji'],
                                            info['title_english'])
            else:
                name = '**{}**'.format(info['title_romaji'])
            await self.bot.say('{}\n{} Episodes - {}\n*{}*\n{}\n{}\n{}'.format(
                name,
                info['total_episodes'],
                info['airing_status'].capitalize(),
                info['description'].replace('<br>', ''),
                info['classification'],
                info['image_url_lge'],
                'http://anilist.co/anime/' + str(info['id'])))

    def _anime_auth(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': 'prappe-o3oux',
            'client_secret': 'Pvpm2wJ0qMTOKnLZoOq49RPFqCLF'
        }
        anime = requests.post('http://anilist.co/api/auth/access_token',
                              params=payload)
        self.anilist_auth = anime.json()
        asyncio.get_event_loop().call_later(self.anilist_auth['expires_in'],
                                            self._anime_auth)
        time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        print("Anilist authentication refreshed:", time)

    @commands.command()
    async def roll(self, *n):
        """Roll a random number."""
        try:
            x = int(n[0])
        except Exception:
            x = 100
        finally:
            y = random.randint(1, 100) if x < 1 else random.randint(1, x)
            await self.bot.say('Rolling 1-{}: **{}**'.format(x, y))

    @commands.command(pass_context=True)
    async def avatar(self, ctx):
        """Return mentioned user's avatar."""
        if len(ctx.message.mentions) > 0:
            await self.bot.say(ctx.message.mentions[0].avatar_url)
        else:
            await self.bot.say(ctx.message.author.avatar_url)

    @commands.command(pass_context=True)
    async def say(self, ctx):
        """Repeat passed message."""
        repeat = ctx.message.content[4:]
        if repeat.startswith("~"):
            print(repeat[1:])
        await self.bot.say(repeat)


def setup(bot):
    """Setup function."""
    bot.add_cog(General(bot))
