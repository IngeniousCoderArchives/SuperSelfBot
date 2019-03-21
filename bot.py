import discord
from discord.ext import commands

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name=str(f"Maplestory")))
  
  
@bot.event
async def on_message(message):
  if message.author.id == 319794228085653506: await bot.process_commands(message)
  
@bot.command(pass_context=True)
async def eval(ctx, *, body: str):
    """Evaluates a code"""

    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'guild': ctx.message.guild,
        'message': ctx.message,
       }
    if ctx.message.author.id == 319794228085653506:
      env.update(globals())

      stdout = io.StringIO()

      to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

      try:
          exec(to_compile, env)
      except Exception as e:
          return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

      func = env['func']
      try:
         with redirect_stdout(stdout):
            ret = await func()
      except Exception as e:
          value = stdout.getvalue()
          await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
      else:
          value = stdout.getvalue()
          try:
              await message.add_reaction('\u2705')
          except:
              pass

          if ret is None:
              if value:
                  await ctx.send(f'```py\n{value}\n```')
          else:
              pass


bot.run(os.environ.get("token"))
