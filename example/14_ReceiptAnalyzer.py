
from loguru import logger
import urllib.request
import datetime
import os
# ロギング設定の例
logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

import sys
import pprint
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

pprint.pprint(sys.path)

# 相対インポートまたは適切なパス設定を検討してください
from api.ConfigLoader import ConfigLoader
from api.CategoryLoader import CategoryLoader
from api.ReceiptAnalyzer import ReceiptAnalyzer

# コンフィグとカテゴリローダーの初期化
config_loader = ConfigLoader()
category_loader = CategoryLoader("data/category.csv")
analyzer = ReceiptAnalyzer(config_loader, category_loader)

target_dir = "sample"
save_dir = f'data/img/{target_dir}'
receipt = analyzer.analyze_receipts(save_dir, target_dir)

print(receipt)