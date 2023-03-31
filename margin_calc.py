import traceback
import cfg
import err_handle
from cfg import DBMS as DBMS
from tqdm import tqdm
import sys


def integrityCheck(i, worldID):
  if "saleVelocity" not in i["marketboard"][str(
      worldID)] or "price" not in i["marketboard"][str(worldID)]:
    cfg.ERRLOG.append(i["_id"] + " i missing marketboard fields in world " +
                      str(worldID))
    return False
  return True


def calcMargin(items, worldID):
  # data = DBMS.dataToDict()
  try:
    for x in tqdm(items):
      i = DBMS.find({"_id": str(x)})
      if i is None:
        print(x)
        sys.exit(1)
      id = i["_id"]

      if i["Recipes"] == "No recipes":
        DBMS.update({"_id": id}, {
          "$set": {
            "marketboard." + str(worldID) + ".profitMargin":
            1,
            "marketboard." + str(worldID) + ".shortProfitIndex":
            i["marketboard"][str(worldID)]["saleVelocity"],
            "containsUntradeable":
            False
          }
        })
        continue
      arrRec = i["Recipes"]
      cost = 0
      contUntrad = False
      for j in arrRec.values():
        for itemID, amount in j["ingredients"].items():
          if itemID == "0":
            continue
          if DBMS.find({"_id": itemID}) is None:
            cost += 0
            contUntrad = True
          else:
            recID = DBMS.find({"_id": itemID})
            cost += recID["marketboard"][str(worldID)]["price"] * amount
      cost = cost / len(arrRec)  #to average the cost
      if i["marketboard"][str(worldID)]["price"] == 0:
        margin = 1
      else:
        margin = (i["marketboard"][str(worldID)]["price"] -
                  cost) / i["marketboard"][str(worldID)]["price"]
      DBMS.update({"_id": id}, {
        "$set": {
          "marketboard." + str(worldID) + ".profitMargin":
          margin,
          "marketboard." + str(worldID) + ".cost":
          cost,
          "marketboard." + str(worldID) + ".shortProfitIndex":
          margin * i["marketboard"][str(worldID)]["saleVelocity"],
          "containsUntradeable":
          contUntrad
        }
      })

  except:
    cfg.ERRLOG.append("Error calculating margin: " + traceback.format_exc())
    print(cfg.FAIL + "Error calculating margin at array" + str(x) + cfg.N)
    print(traceback.format_exc())
    err_handle.errExit()
    sys.exit(1)


def optimizedMargin(items, worldID):
  # this function will make an optimized cost based on shop price, will need to figure out how to append items based on shop or other, but thats for another day
  # WILL NEED:
  # TO COLLECT WORLD INFORMATION, maybe outside information that shows the lowest value amongst worlds?
  # PLEASE USE . NOTATION (ex: "marketboard.75.cost") AS YOUR KEYS WHEN UPDATING OR ELSE IT WILL OVERWRITE ***EVERYTHING*** UNDER THAT FIELD
  pass
