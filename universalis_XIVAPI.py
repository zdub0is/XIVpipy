import traceback
import cfg
from tqdm import trange
import api_call
from cfg import DBMS as DBMS
import sys
import err_handle
from discord_rprt import post_message as WH

def checkKey(di):
  if "jobs" in di:
    return False
  else:
    return True

def priceGrab(xivjson, dicTemp):
  if xivjson["PriceMid"] == 99999:
    dicTemp["shopPrice"] = 0
  else:
    dicTemp["shopPrice"] = xivjson["PriceMid"]
  if "PriceLow" in xivjson:
    dicTemp["shopSellPrice"] = xivjson["PriceLow"]
  return dicTemp

def recipeMake(xivjson):
  mainArr = dict()
  arrRec = xivjson["Recipes"]
  for a in range(len(arrRec)):
    recjson = api_call.apiCall(cfg.XIVRECIPE + str(arrRec[a]["ID"]))
    rectemp = dict()
    for b in range(10):
      if recjson["ItemIngredient" + str(b) + "TargetID"] != 0:
        rectemp[str(recjson["ItemIngredient" + str(b) +
                          "TargetID"])] = recjson["AmountIngredient" +
                                                  str(b)]
    mainArr[str(arrRec[a]["ID"])] = {"job": recjson["ClassJob"]["ID"], "lvl":   recjson["RecipeLevelTable"]["ClassJobLevel"], "ingredients": rectemp}
  return mainArr

def XIVAPIprocess(itemID, dicTemp):
  check = DBMS.find({"_id":itemID})
  if check is None:
    # print(check, itemID, dicTemp)
    xivjson = api_call.apiCall(cfg.XIVITEM + str(itemID))
    dicTemp["Name"] = xivjson["Name"]
    if "Recipes" in xivjson:
      dicTemp["Recipes"] = recipeMake(xivjson)
    else:
      dicTemp["Recipes"] = "No recipes"
    dicTemp = priceGrab(xivjson, dicTemp)
    DBMS.insert(dicTemp)
    return
  elif "Recipes" not in check:
    xivjson = api_call.apiCall(cfg.XIVITEM + str(itemID))
    if "Recipes"in xivjson:
      dicTemp["Recipes"] = recipeMake(xivjson)
    dicTemp = priceGrab(xivjson, dicTemp)
  if "shopPrice" not in check and "shopPrice" not in dicTemp:
    xivjson = api_call.apiCall(cfg.XIVITEM + str(itemID))
    dicTemp = priceGrab(xivjson, dicTemp)
  delet = dicTemp.pop("_id")
  DBMS.update({"_id": delet}, {"$set": dicTemp})

def main(worldID):
  print("Starting Queries for", str(worldID))
  # add discord rprt here
  loopGo = cfg.ITEM_LIST
  for _ in trange(cfg.NUMLOOP):
    temp = loopGo[0:cfg.NUMSEND + 1]
    # add last updated timestamp to database
    if len(loopGo) == 0:
      break
    for i in range(len(temp)):
      loopGo.pop(0)
    try:
      url = cfg.UNISTART + str(worldID) + "/" + ",".join(map(str, temp)) + cfg.UNIEND
      j = api_call.apiCall(url)
      try:
        for h in range(len(temp)):
          dicTemp = {
            "_id": temp[h],
            "marketboard." + str(worldID) + ".price" : 0,
             "marketboard." + str(worldID) + ".overallAverage" : 0,
             "marketboard." + str(worldID) + ".saleVelocity" : 0,
             "marketboard." + str(worldID) + ".currentAverage" : 0
          }
          
          dicTemp["_id"] = str(temp[h])
          if str(temp[h]) not in j["items"]:
            # dicTemp["marketboard"][str(worldID)]["price"] = 0
            # dicTemp["marketboard"][str(worldID)]["overallAverage"] = 0
            # dicTemp["marketboard"][str(worldID)]["saleVelocity"] = 0
            # dicTemp["marketboard"][str(worldID)]["currentAverage"] = 0
            XIVAPIprocess(str(temp[h]), dicTemp)
            continue
          dicTemp["marketboard." + str(worldID) + ".price"] = j["items"][str(temp[h])]["minPrice"]
          dicTemp["marketboard." + str(worldID) + ".overallAverage"] = j["items"][str(temp[h])]["averagePrice"]
          dicTemp["marketboard." + str(worldID) + ".saleVelocity"] = j["items"][str(temp[h])]["regularSaleVelocity"]
          dicTemp["marketboard." + str(worldID) + ".currentAverage"] = j["items"][str(temp[h])]["currentAveragePrice"]

          XIVAPIprocess(str(temp[h]), dicTemp)
      except:
        cfg.ERRLOG.append("Json was not readable for array" + str(temp[0]) + " " +
                      str(temp[-1]))
        print(cfg.FAIL + cfg.ERRLOG[-1] + cfg.N)
        print(url)
        print(dicTemp)
        print(traceback.format_exc())  
    except Exception as err:
      cfg.ERRLOG.append(traceback.format_exc())
      err_handle.errExit()
      print(err, temp)
      sys.exit(traceback.format_exc())
  
  WH("Market data has been aggregated/updated.")
  print(cfg.OKGREEN + "Successfully updated market data" + cfg.N)
  #add discord report here