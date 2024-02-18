import sys
import pprint
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

pprint.pprint(sys.path)

from api.ConfigLoader import ConfigLoader
from api.CategoryLoader import CategoryLoader
from api.ReceiptAnalyzer import ReceiptAnalyzer

if __name__ == "__main__":
    config_loader = ConfigLoader()
    category_loader = CategoryLoader("data/category.csv")
    analyzer = ReceiptAnalyzer(config_loader, category_loader)
    analyzer.analyze_receipts("data/img")