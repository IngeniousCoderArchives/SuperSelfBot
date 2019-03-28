import discord
import os
from discord.ext import commands
import io, traceback, textwrap
from contextlib import redirect_stdout
bot = commands.Bot(command_prefix=os.environ.get("prefix").replace("\"",""),description="An Instance of XtremeCoder's SuperSelfBot, https://github.com/IngeniousCoder/SuperSelfBot")
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game(name=str(os.environ.get("game"))))
  
  
@bot.event
async def on_message(message):
  if message.author.id == int(os.environ.get("owner")): await bot.process_commands(message)
  

@bot.command()
async def embed(ctx,*,flags):
    """Sends an embed.
    Flags :
    author - set the author name
    icon - set the icon
    field:fieldname> - creates a field
    footer - set the footer
    footericon - set the footer icon
    desc - set thee desc
    title - set the embed title
    colour - set the embed colour
    thumbnail - set the thumbnail 
    image - set the image

    Example :
    [prefix]embed -title Testing Embed -desc Hi testing
    """
    flags = flags.split("-")
    embed = discord.Embed()
    for flag in flags:
        flag_name = flag.split(" ")[0].lower()
        try:
          flag_content = flag.split(" ",1)[1]
        except:
          continue
        if flag_name == "author":
            if embed.author.icon_url == discord.Embed.Empty:
                embed.set_author(name=flag_content)
            else:
                embed.set_author(name=flag_content,icon_url=embed.author.icon_url)
        if flag_name == "icon":
            if embed.author.name == discord.Embed.Empty:
                embed.set_author(name="",icon_url=flag_content)
            else:
                embed.set_author(name=embed.author.name,icon_url=flag_content)
        if flag_name.startswith("field"):
            # determine name of field
            name = flag.split(":")[1]
            name = name.split(">")[0]
            embed.add_field(name=name,value=flag.split(">")[1])
        if flag_name == "footer":
            if embed.footer.icon_url == discord.Embed.Empty:
                embed.set_footer(text=flag_content)
            else:
                embed.set_footer(text=flag_content,icon_url=embed.footer.icon_url)       
        if flag_name == "footericon":
            if embed.footer.text == discord.Embed.Empty:
                embed.set_footer(text="",icon_url=flag_content)
            else:
                embed.set_footer(icon_url=flag_content,text=embed.footer.text)
        if flag_name == "desc":
            embed.description = flag_content
        if flag_name == "title":
            embed.title = flag_content
        if flag_name == "colour":
            embed.colour = discord.Color(value=int(flag_content,16))
        if flag_name == "thumbnail":
            embed.set_thumbnail(url=flag_content)
        if flag_name == "image":
            embed.set_image(url=flag_content)
    await ctx.send(embed=embed)
    await ctx.message.delete()
  
@bot.command()
async def send(ctx,*,message):
    """Send something and deletes the command message"""
    await ctx.message.delete()
    await ctx.send(message)
    
    
@bot.command()
async def game(ctx,*,name):
    """Set game"""
    await bot.change_presence(activity=discord.Game(name=str(name)))
    
    

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
    if ctx.message.author.id == int(os.environ.get("owner")):
      await ctx.message.delete()
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
