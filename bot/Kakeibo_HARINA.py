import discord
from discord.ext import commands
from loguru import logger
import urllib.request
import datetime
import os
import sys
import pprint
import requests
import json
import shutil

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

logger.add("log/debug.log", format="{time} {level} {message}", level="DEBUG")

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
pprint.pprint(sys.path)

from api.ConfigLoader import ConfigLoader
from api.CategoryLoader import CategoryLoader
from api.ReceiptAnalyzer import ReceiptAnalyzer

config_loader = ConfigLoader()
category_loader = CategoryLoader("data/category.csv")
analyzer = ReceiptAnalyzer(config_loader, category_loader)

TOKEN = os.getenv('DISCORD_BOT_TOKEN_HARINA')
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def send_data_to_gas(json_data, tag, file_name):
    url = os.environ['GAS_JSON2GSS_URL']
    headers = {'Content-Type': 'application/json'}
    data = {
        'json_data': json_data,
        'tag': tag,
        'file_name': file_name
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info(f"{file_name} is {response.text}")

def get_target_dir(channel_id):
    return "maki" if channel_id == 1208743619029368836 else "sample"

async def save_image(url, save_dir, file_name):
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, os.path.join(save_dir, file_name))
        return True
    except Exception as e:
        logger.error(f"画像の保存に失敗しました: {e}")
        return False

async def process_attachments(message):
    target_dir = get_target_dir(message.channel.id)
    save_dir = f'data/img/{target_dir}'

    for attachment in message.attachments:
        url = attachment.url
        date = datetime.datetime.now()
        file_name = f"{date.strftime('%Y%m%d%H%M%S')}_{attachment.filename}".replace(".jpg.jpg", ".jpg")
        
        if await save_image(url, save_dir, file_name):
            await message.channel.send(f"画像を保存しました: {file_name}")
            logger.info(f"画像を保存しました: {file_name}")
        else:
            await message.channel.send("画像の保存に失敗しました。")
            logger.info("画像の保存に失敗しました。")
    
    receipt = analyzer.analyze_receipts(save_dir, target_dir)
    await message.channel.send(f"```{receipt}```")

    output_folder = 'output'
    archive_folder = 'archive'
    os.makedirs(archive_folder, exist_ok=True)

    for root, dirs, files in os.walk(output_folder):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    json_data = json.load(file)
                    tag = os.path.basename(os.path.dirname(file_path))
                    send_data_to_gas(json_data, tag, file_name)
                
                # JSONファイルをarchiveフォルダに移動
                archive_path = os.path.join(archive_folder, tag)
                os.makedirs(archive_path, exist_ok=True)
                shutil.move(file_path, os.path.join(archive_path, file_name))

    # imgフォルダ内の画像ファイルを削除
    for root, dirs, files in os.walk(save_dir):
        for file_name in files:
            if file_name.endswith('.jpg'):
                file_path = os.path.join(root, file_name)
                os.remove(file_path)

@bot.event
async def on_ready():
    logger.info("ログインしました")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == '/harina':
        await message.channel.send('ちゅん')
        logger.info(f"channel id: {message.channel.id}")
    
    if message.attachments:
        logger.info(f"channel id: {message.channel.id}")
        await process_attachments(message)
    else:
        await message.channel.send("添付ファイルが見つかりません。")

bot.run(TOKEN)