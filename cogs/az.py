#!/usr/bin/env python3

import re
import asyncio
import discord
import os
from discord.ext import commands
from cogs.utils.format import *
from cogs.utils import perms
from cogs.utils import puush
from cogs.utils import find as azfind
from cogs.utils.config import Config


class AZ:
  def __init__(self, bot):
    self.bot  = bot
    self.conf = Config('configs/az.json')

  @commands.command()
  async def lenny(self, first=''):
    try:
      num = int(first)
      if num < 1:
        num = 1
      if num > 10:
        num = 10
    except:
      num = 1
    if num == 1 and first.lower() in self.conf['lenny']:
      await self.bot.say(code(self.conf['lenny'][first]))
    else:
      await self.bot.say('\n( ͡° ͜ʖ ͡° )'*num)

  @commands.command()
  async def shrug(self):
    await self.bot.say('\n¯\_(ツ)_/¯')

  @commands.command(pass_context=True)
  async def me(self, ctx, *, message : str):
    await self.bot.say('*{} {}*'.format(ctx.message.author.name, message))
    try:
      await self.bot.delete_message(ctx.message)
    except:
      pass

  @commands.command(pass_context=True,name='set_colour',aliases=['sc'])
  @perms.is_in_servers('168702989324779520')
  @perms.has_role_check(lambda r: r.id == '258405421813989387')
  async def _set_colour(self, ctx, colour):
    """
    set role colour

    colour can be a hex value or a name:
    teal         0x1abc9c.
    dark_teal    0x11806a.
    green        0x2ecc71.
    dark_green   0x1f8b4c.
    blue         0x3498db.
    dark_blue    0x206694.
    purple       0x9b59b6.
    dark_purple  0x71368a.
    magenta      0xe91e63.
    dark_magenta 0xad1457.
    gold         0xf1c40f.
    dark_gold    0xc27c0e.
    orange       0xe67e22.
    dark_orange  0xa84300.
    red          0xe74c3c.
    dark_red     0x992d22.
    lighter_grey 0x95a5a6.
    dark_grey    0x607d8b.
    light_grey   0x979c9f.
    darker_grey  0x546e7a.
    """
    cols = {
      'teal' : discord.Colour.teal(),
      'dark_teal' : discord.Colour.dark_teal(),
      'green' : discord.Colour.green(),
      'dark_green' : discord.Colour.dark_green(),
      'blue' : discord.Colour.blue(),
      'dark_blue' : discord.Colour.dark_blue(),
      'purple' : discord.Colour.purple(),
      'dark_purple' : discord.Colour.dark_purple(),
      'magenta' : discord.Colour.magenta(),
      'dark_magenta' : discord.Colour.dark_magenta(),
      'gold' : discord.Colour.gold(),
      'dark_gold' : discord.Colour.dark_gold(),
      'orange' : discord.Colour.orange(),
      'dark_orange' : discord.Colour.dark_orange(),
      'red' : discord.Colour.red(),
      'dark_red' : discord.Colour.dark_red(),
      'lighter_grey' : discord.Colour.lighter_grey(),
      'dark_grey' : discord.Colour.dark_grey(),
      'light_grey' : discord.Colour.light_grey(),
      'darker_grey' : discord.Colour.darker_grey()
    }
    colour = colour.lower().strip()
    m      = re.search('^(0[hx])?([a-f0-9]{6})$', colour)
    if colour in cols:
      c = cols[colour]
    elif m:
      c = discord.Colour(int(m.group(2), 16))
    else:
      await self.bot.say('could not find valid colour, see help')
      return

    server = ctx.message.server
    for role in server.roles:
      if role.id == '258405421813989387':
        await self.bot.edit_role(server, role, colour=c)
        await self.bot.say(ok())
        return
    await self.bot.say('could not find role to change')

  @commands.command(pass_context=True)
  @perms.in_group('img')
  async def img(self, ctx, *search):
    if 'path' not in puush.conf or not os.path.exists(puush.conf['path']):
      await self.bot.say('{path} does not exist')
      return

    search = [re.sub(r'[^\w\./#\*-]+', '', i).lower() for i in search]
    for i in range(len(search)):
      if re.search('^(//|#)', search[i]):
        search = search[:i]
        break

    for i in range(len(search)):
      if re.search('^(/\\*)', search[i]):
        for j in range(i, len(search)):
          if re.search('^(\\*/)', search[j]):
            break
        search = search[:i] + search[j+1:]
        break

    loop = asyncio.get_event_loop()
    try:
      f = loop.run_in_executor(None, azfind.search, puush.conf['path'], search)
      path = await f
    except:
      path = ''

    if not path or not path.strip():
      await self.bot.send_message(ctx.message.channel,
                          "couldn't find anything matching: `{}`".format(search)
      )
      return

    try:
      future_url = loop.run_in_executor(None, puush.get_url, path)
      url = await future_url
    except:
      url = 'There was an error uploading the image, ' + \
            'but at least I didn\'t crash :p'
    await self.bot.say(url)

def setup(bot):
  bot.add_cog(AZ(bot))
