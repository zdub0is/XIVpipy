import os
import time
import dbms
# DO NOT TOUCH ANYTHING IN THIS MODULE, THESE ARE GLOBAL VARIABLES FOR USE BY EVERY MODULE

OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
N = '\033[0;0m'
ERRLOG = []
UNISTART = "https://universalis.app/api/v2/"
UNIEND = "?fields=items.itemID%2Citems.currentAveragePrice%2Citems.regularSaleVelocity%2Citems.averagePrice%2Citems.minPrice"
UNIHIST = "https://universalis.app/api/v2/history/"
MARKETABLE = "https://universalis.app/api/v2/marketable/"
WEBHOOK = os.environ['discWH']
XIVITEM = "https://xivapi.com/item/"
XIVRECIPE = "https://xivapi.com/recipe/"
TWOMONTHS = int(time.time() - 60 * 60 * 24 * 60)
WORLDS =  ["34", "37", "41", "62", "74", "75", "81", "91"]
ITEM_LIST = []
LEN_LIST = 0
NUMSEND = 0
NUMLOOP = 0
DBMS = dbms.DBMS()