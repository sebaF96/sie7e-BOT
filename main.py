import os
import time
from discord.ext import commands
from cogs.dota.dota import Dota2
from cogs.among import AmongUS
from cogs.events import Events
from cogs.misc import Misc


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
bot.remove_command('help')


if __name__ == '__main__':
    bot.add_cog(Events(bot))
    bot.add_cog(Dota2(bot))
    bot.add_cog(AmongUS(bot))
    bot.add_cog(Misc(bot, start_time=int(time.time())))

    bot.run(os.getenv('BOT_TOKEN'))
