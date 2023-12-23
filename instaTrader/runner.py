from datetime import datetime
from time import sleep
import os



while str(datetime.now())[8:16] != "22 19:29":
    sleep(1)

os.system("py instaTrader.py")