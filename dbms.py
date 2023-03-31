import os
import traceback
from pymongo import MongoClient
import cfg
import err_handle
import sys 
import json
from pymongo import ReturnDocument
from discord_rprt import post_message as WH
from tqdm import tqdm

class DBMS:
  def __init__(self):
    self.client = MongoClient("mongodb+srv://zubos:"+ os.environ['DBMSPW'] +"@items.645ingm.mongodb.net/?retryWrites=true&w=majority")
    self.db = self.client.contentV2
    self.conn = self.db.items

  def find(self, query):
    try:
      return self.conn.find_one(query)
    except:
      self.err(traceback.format_exc())

  def insert(self, query):
    try:
      self.conn.insert_one(query)
    except:
      self.err(traceback.format_exc())
#{"_id":"2","Name":"Fire Shard","Recipes":"No recipes","shopPrice":{"$numberInt":"9"},"shopSellPrice":{"$numberInt":"0"},"containsUntradeable":false,"profitMargin":{"$numberInt":"1"}}

  
  def update(self, id, update):
    try:
      self.conn.find_one_and_update(id, update, return_document= ReturnDocument.AFTER)
      # 
    except:
      self.err(traceback.format_exc())

  def ping(self):
    if self.db.command("ping")['ok'] == 1:
      print("PyMongo is successfully responding.")
    else:
      cfg.ERRLOG.append('PyMongo is not responding. Please check the connection.')
      err_handle.handle_err()
      sys.exit(1)

  def removeRecipe(self):
    self.conn.update_many({}, {"$unset": {'profitMargin': ''}})
    print("Recipes have been removed.")

  def dataToDict(self):
    d = dict()
    for document in self.conn.find({}):
      d[document['_id']] = document
    return d

  def export(self, worldID, recipeExport):
    exportType = "with recipes" if recipeExport else "without recipes"
    print(cfg.WARNING + "Beginning export process "+ exportType + ", please wait..." + cfg.N)
    
    stora = []
    item = {}
    # {$and: [{Recipes: {$ne: "No recipes"}}, {marketboard.75.shortProfitIndex: {"$gte": 0.5}}]}
    if recipeExport:
      items = self.conn.find({"$and": [{"Recipes": {"$ne": "No recipes"}},{"marketboard." + str(worldID) + ".shortProfitIndex": {"$gte": 2}}]}).sort("marketboard." + str(worldID) + ".shortProfitIndex", -1) #find based on worldID called
    else:
      items = self.conn.find({"$and": [{"Recipes": "No recipes"},{"marketboard." + str(worldID) + ".shortProfitIndex": {"$gte": 2}}]}).sort("marketboard." + str(worldID) + ".shortProfitIndex", -1)
    try:
      for item in tqdm(items):
        temp = {"name": item["Name"], "profitIndex": item["marketboard"][str(worldID)]["shortProfitIndex"], "price" :item["marketboard"][str(worldID)]["price"]} #make part of temp
        if "cost" in item["marketboard"][str(worldID)]:
          temp["cost"] = item["marketboard"][str(worldID)]["cost"]
        if "shopSellPrice" in item:
          temp["shopSellPrice"] = item["shopSellPrice"]
        rec = []
        if item["Recipes"] != "No recipes":
          for j in item["Recipes"].values():
            rec.append(dict())
            rec[-1]["Crafter ID"] = j["job"]
            rec[-1]["Level Required"] = j["lvl"]
            rec[-1]["Ingredients"] = []
            
            for x, y in j["ingredients"].items():
              if x == "0":
                continue
              r = self.conn.find_one({"_id": x})
              if r is None:
                rec[-1]["Ingredients"].append({"name": x})
                continue
              if "cost" in r:
                rec[-1]["Ingredients"].append({"name": r["Name"], "amount": y, "price": (r["marketboard"][str(worldID)]["price"] * y), "cost": r["marketboard"][str(worldID)]["cost"]})
              else:
                rec[-1]["Ingredients"].append({"name": r["Name"], "amount": y,"price": (r["marketboard"][str(worldID)]["price"] * y)})
          # print(rec)
          temp["Recipes"] = rec
        stora.append(temp)
      if recipeExport:
        fileName = "./jsons/" + str(worldID) + "data.json"
      else:
        fileName = "./jsons/" + str(worldID) + "dataNOREC.json"
      
      with open(fileName, "w") as f:
        json.dump(stora, f)
  
      print("done")
    except:
      print(item)
      self.err(traceback.format_exc())

  def err(self, err):
    cfg.ERRLOG.append(err)
    err_handle.errExit()
    sys.exit(1)