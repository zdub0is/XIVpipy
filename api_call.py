import requests
from requests import HTTPError
import traceback
from err_handle import errExit
import sys
import cfg

def apiCall(url):
  try:
    r = requests.get(url)
    x = 0
    while not r.ok:
      x += 1
      cfg.ERRLOG.append("Status Code: " + str(r.status_code) + ", Retry #" +
                    str(x) + ", on Array starting at " + url)
      print(cfg.WARNING + cfg.ERRLOG[-1] + cfg.N)
      r = requests.get(url)
      if x == 10:
        raise HTTPError("URL failed to respond at " + url)
      if r.ok:
        cfg.ERRLOG.append("Retry #" + str(x) + " successful, going to next.")
        print(cfg.OKGREEN + cfg.ERRLOG[-1] + cfg.N)
    if r.ok:
      return r.json()
  except:
    cfg.ERRLOG.append("Failed to get JSON from API call at " + url)
    errExit()
    print(traceback.format_exc())
    sys.exit(1)