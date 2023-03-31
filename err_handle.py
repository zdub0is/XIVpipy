
from discord_rprt import rprt
import cfg
import sys
def errExit():
  rprt("ERROR")
  errRecord()
  sys.exit(1)

def errRecord():
  with open('errLog.txt', 'w') as f:
    f.write('/n'.join(cfg.ERRLOG))