import io
import discord
import aiohttp
import openai
import os
import logging
from discord.ext import commands
import asyncio

openai.api_key = os.environ.get("OPENAI_API_KEY")
discord_api_key = os.environ.get("DISCORD_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()
        
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
    )
    return response.data[0].url
        
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if bot.user not in message.mentions:
        return

    prompt = message.content.replace(f'<@!{bot.user.id}>', '').strip()

    print("user prompt: ", prompt)

    if not prompt:
        return
    
    loop = asyncio.get_event_loop()
    
    url = await loop.run_in_executor(None, generate_image, prompt)

    print("image url: ", url)

    image = await download_image(url)

    image = discord.File(fp=io.BytesIO(image), filename='image.png')
    await message.channel.send(file=image)

bot.run(discord_api_key)
