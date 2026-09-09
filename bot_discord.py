import discord
import random
import os
import requests
from discord.ext import commands
from model import get_class

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

praticas = ["Faça separação do seu lixo", "Diminua o uso de descartáveis", "Não descarte pilhas e baterias em lixo comum", "Reduza o consumo de água", "escolha embalagens reutilizáveis","Mantenha as lâmpadas ligadas apenas quando necessário"]

@bot.event
async def on_ready():
    print(f'Fizemos login como {bot.user}')

@bot.command()
async def ajuda(ctx):
        await ctx.send("""
📌 Lista de Comandos do Bot

👋 hello
→ Eu apenas digo olá e informo meu nome.

👋 bye
→ Envio um emoji para me despedir de você.

😂 heh [número]
→ Quanto maior o número, mais eu vou rir!

📅 joined @usuário
→ Mostra há quanto tempo a pessoa mencionada está no servidor.

🎲 roll NdN
→ Rola dados no formato RPG.
Exemplo: $roll 1d6 (1 dado com 6 lados)

🤣 meme
→ manda um meme aleatorio.
                       
🦆 duck
→ manda uma imagem aleatoria de um pato
                       
🐶 dog
→ manda uma imagem aleatoria de um cachorro
                       
♻️ dicas
→ Eu cito algumas praticas sustentaveis

🌲 praticar
→ Eu vou enviar uma pratica sustentavel aleatoria para você executar
                  
---
💡 Use os comandos com o prefixo $
""")

@bot.command()
async def hello(ctx):
    await ctx.send(f"ola eu sou: {bot.user}")

@bot.command()
async def bye(ctx):
    await ctx.send("\U0001f642")

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')

@bot.command()
async def roll(ctx, dice: str):
    """Rola dados em formado NdN"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send("Não esta em formato NdN")
        return
    
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir("images"))
    with open(f'images/{img_name}', 'rb') as f:
        #Vamos armazenar o arquivo convertido da biblioteca do Discord nesta variável!
        picture = discord.File(f)
    # Podemos então enviar esse arquivo como um parâmetro
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Uma vez que chamamos o comando duck, o programa chama a função get_duck_image_url '''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command('dog')
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

@bot.command()
async def dicas(ctx):
    await ctx.send("""
♻️→ Redução de Desperdícios (5 Rs): Repensar, recusar, reduzir, reutilizar e reciclar.
                   
💧→ Uso Consciente da Água: Fechar torneiras, consertar vazamentos e reutilizar água da máquina de lavar.

⚡→ Eficiência Energética: Apagar luzes, substituir por lâmpadas LED e tirar aparelhos da tomada.
                   
🌲→ Consumo Sustentável: Levar sacolas reutilizáveis, evitar plásticos de uso único (canudos, copos) e preferir produtos a granel.
                   
🍔→ Alimentação e Compostagem: Reduzir desperdício de comida, comprar de produtores locais e compostar resíduos orgânicos
""")
    
@bot.command()
async def praticar(ctx):
    pratica = random.choice(praticas)
    await ctx.send(pratica)

@bot.command()
async def check(ctx):
    if ctx.message.attachment:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_class(model_path="./keras_model.h5", labels_path="./labels.txt", image_path=f"./{attachment.filename}"))
    else:
        await ctx.send("Você não enviou nenhuma imagem. Por favor, envie uma imagem para que eu possa verificar.")

bot.run("TOKEM")
