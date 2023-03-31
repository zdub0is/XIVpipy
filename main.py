import schedule
import time
from margin_calc import calcMargin
import universalis_XIVAPI as uXIVAPI
from multiprocessing import Process
import multiprocessing
from discord_rprt import post_message as WH

#modules in this dir
import cfg
from api_call import apiCall

def factors(x, max):
  arr = []
  for i in range(1, x + 1):
    if x % i == 0:
      arr.append(i)
  return arr[min(range(len(arr)), key=lambda i: abs(arr[i]-max))], arr[(-1 * min(range(len(arr)), key=lambda i: abs(arr[i]-max))) -1]

# def marginThreads(worldID):
#   #these numbers will have to be adjusted later based on updates, figure out a way to modify it
#   WH("Beginning Margin calculations for World ID: " + str(worldID))
#   print(cfg.OKCYAN + "Beginning Margin Calculations" + cfg.N)
#   t1 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[0:2003], worldID, ))
#   t2 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[2003:4005], worldID, ))
#   t3 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[4005:6006], worldID, ))
#   t4 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[6006:8009], worldID, ))
#   t5 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[8009:10010], worldID, ))
#   t6 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[10010:12012], worldID, ))
#   t7 = threading.Thread(target=calcMargin, args=(cfg.ITEM_LIST[12012:], worldID, ))
#   print(cfg.OKBLUE + "Opening Threads" + cfg.N)
#   t1.start()
#   t2.start()
#   t3.start()
#   t4.start()
#   t5.start()
#   t6.start()
#   t7.start()


def universalisThreads(worlds = cfg.WORLDS):    
  WH("Beginning Universalis Queries")
  for n in range(0, len(worlds), 2):
    threads = []
    for i in worlds[n:n+2]:
      t = Process(target=uXIVAPI.main, args=(i, ))
      threads.append(t)
      t.start()
    for t in threads:
      t.join()
  WH("Universalis Queries Complete")

def marginThreadsV2(wID):
  WH("Beginning Margin calculations for World ID: " + str(wID))
  x, y = factors(cfg.LEN_LIST, 7)
  inputs = []
  threads = []
  for i in range(0, cfg.LEN_LIST, y):
    inputs.append(cfg.ITEM_LIST[i:i+y])
  for n in range(len(inputs)):
    t = Process(target=calcMargin, args=(inputs[n], wID, ))
    threads.append(t)

  for t in threads:
    t.start()
  for t in threads:
    t.join()
  WH("Margin calculations for World ID: " + str(wID) + " complete!")
  
# def runtime():
#   universalisThreads()
#   for h in cfg.WORLDS:
#     marginThreadsV2(h)
#     cfg.DBMS.export(h, True)
#     cfg.DBMS.export(h, False)

def __main__():
  # get item list from MARKETABLE using api_call
  # input("Once complete, press enter...")
  print("Starting calculation process...")
  cfg.ITEM_LIST = apiCall(cfg.MARKETABLE)
  cfg.LEN_LIST = len(cfg.ITEM_LIST)
  cfg.NUMSEND, cfg.NUMLOOP = factors(cfg.LEN_LIST, 100)
  print(cfg.NUMSEND, cfg.NUMLOOP)
  cfg.DBMS 
  cfg.DBMS.ping()
  universalisThreads()
  for h in cfg.WORLDS:
    marginThreadsV2(h)
    WH("Beginning export for World ID: " + str(h))
    cfg.DBMS.export(h, True)
    cfg.DBMS.export(h, False)
    WH("Exporting complete for World ID: " + str(h))
  # uXIVAPI.main(cfg.WORLDS[5])
  # marginThreads(cfg.WORLDS[5])
  # marginThreadsV2(cfg.WORLDS[5])
  
  
  # DO NOT NEST
  

__main__()
schedule.every().day.at("08:00").do(__main__)
  # malbor is cfg.WORLDS[5]
print("Use \'kill 1\' in the shell to exit.")
while 1:
  schedule.run_pending()
  time.sleep(1)