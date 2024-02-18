import discord
import os
from loguru import logger
import urllib.request
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

import sys
import pprint
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

pprint.pprint(sys.path)

from api.ConfigLoader import ConfigLoader
from api.CategoryLoader import CategoryLoader
from api.ReceiptAnalyzer import ReceiptAnalyzer

config_loader = ConfigLoader()
category_loader = CategoryLoader("data/category.csv")
analyzer = ReceiptAnalyzer(config_loader, category_loader)


TOKEN = os.getenv('DISCORD_BOT_TOKEN_HARINA')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info("ログインしました")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/harina':
        await message.channel.send('ちゅん')
        logger.info("channel id : ".format(message.channel.id))
    
        
    if message.attachments:
        for attachment in message.attachments:
            url = attachment.url
            date = datetime.datetime.now()
            file_name = f"{date.strftime('%Y%m%d%H%M%S')}_{attachment.filename}.jpg".replace(".jpg.jpg",".jpg")
            save_dir = 'data/img'
            
            # 保存ディレクトリが存在するか確認し、なければ作成
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            try:
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, os.path.join(save_dir, file_name))
                await message.channel.send(f"画像を保存しました: {file_name}")
            except Exception as e:
                logger.error(f"画像の保存に失敗しました: {e}")
                await message.channel.send("画像の保存に失敗しました。")
        
        receipt = analyzer.analyze_receipts("data/img", "maki")
        await message.channel.send("```{}```".format(receipt))
    else:
        await message.channel.send("添付ファイルが見つかりません。")

client.run(TOKEN)
