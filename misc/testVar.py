
from dotenv import load_dotenv, find_dotenv
import os
### give the full path
path='/home/swampi/SwampertReloaded/misc/sample.env'

load_dotenv(dotenv_path=path,verbose=True)

tg_token = os.getenv("TELEGRAMTOKEN")
print(str(tg_token))

