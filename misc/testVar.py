from dotenv import load_dotenv
import os

load_dotenv()

tg_token = os.getenv("TELEGRAMTOKEN")
print(tg_token)