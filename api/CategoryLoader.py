import pandas as pd

class CategoryLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.categories = self.load_categories()

    def load_categories(self):
        df = pd.read_csv(self.filepath, header=None, names=['category'])
        return df['category'].str.cat(sep=',')

