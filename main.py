import discord
from discord.ext import commands
from discord import app_commands
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
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizados {len(synced)} comando(s)")
    except Exception as e:
        print(e)

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

# Comando Slash /fpl
@bot.tree.command(name='fpl', description='Plano de Voo - FBR')
@app_commands.describe(
    numero_voo="Número do Voo",
    nivel_voo="Nível de Voo",
    aeronave="Aeronave",
    tipo_voo="Tipo de Voo (IFR ou VFR)",
    partida="Aeroporto de Partida",
    destino="Aeroporto de Destino",
    horario="Horário de Partida"
)
@app_commands.choices(tipo_voo=[
    app_commands.Choice(name="IFR", value="IFR"),
    app_commands.Choice(name="VFR", value="VFR")
])
async def fpl(
    interaction: discord.Interaction,
    numero_voo: str,
    nivel_voo: str,
    aeronave: str,
    tipo_voo: app_commands.Choice[str],
    partida: str,
    destino: str,
    horario: str
):
    """Cria um plano de voo"""
    
    # Cria o embed com as informações
    embed = discord.Embed(
        title="✈️ Plano de Voo - FBR",
        color=discord.Color.blue()
    )
    
    # Piloto = quem digitou o comando
    embed.add_field(name="👨‍✈️ Piloto", value=f"@{interaction.user.name}", inline=False)
    embed.add_field(name="🔢 Número de Voo", value=numero_voo, inline=False)
    embed.add_field(name="☁️ Nível de Voo", value=nivel_voo, inline=False)
    embed.add_field(name="✈️ Aeronave", value=aeronave, inline=False)
    embed.add_field(name="📡 Tipo de Voo", value=tipo_voo.value, inline=False)
    embed.add_field(name="🛫 Partida", value=partida, inline=False)
    embed.add_field(name="🛬 Destino", value=destino, inline=False)
    embed.add_field(name="🕐 Horário", value=horario, inline=False)
    
    await interaction.response.send_message(embed=embed)

# Roda o bot
if __name__ == '__main__':
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("DISCORD_TOKEN não configurada nas variáveis de ambiente!")
    bot.run(token)
