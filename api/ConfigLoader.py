# from dotenv import load_dotenv
import os

class ConfigLoader:
    def __init__(self, env_path=".env"):
        self.env_path = env_path
        self.config = {}
        self.load_env()

    def load_env(self):
        # load_dotenv(self.env_path)
        self.config['API_KEY'] = os.getenv("GOOGLE_AI_STUDIO_API_KEY")