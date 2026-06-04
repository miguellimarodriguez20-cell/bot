import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Eventos do bot
@bot.event
async def on_ready():
    print(f'{bot.user} está online!')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name="🤖 Bot Ativo 24/7"))

@bot.event
async def on_message(message):
    # Ignora mensagens do próprio bot
    if message.author == bot.user:
        return
    
    # Processa comandos
    await bot.process_commands(message)

# Comando de teste
@bot.command(name='ping')
async def ping(ctx):
    """Retorna o ping do bot"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! {latency}ms')

@bot.command(name='hello')
async def hello(ctx):
    """Saudação do bot"""
    await ctx.send(f'Olá {ctx.author.mention}! 👋')

@bot.command(name='status')
async def status(ctx):
    """Status do bot"""
    await ctx.send(f'✅ Bot está online e funcionando!')

# Roda o bot
if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN não configurada nas variáveis de ambiente!")
    bot.run(token)
