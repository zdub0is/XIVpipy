#################################################################################
#                         NONE OF THIS IS USED ANYMORE                          #
#################################################################################


# def XIVAPIprocess(item, dicTemp):
#   if DBMS.find({"_id": dicTemp["_id"]}) is None:
#     xivjson = api_call.apiCall(cfg.XIVITEM + str(item), )
#     dicTemp["Name"] = xivjson["Name"]
#     if "Recipes" in xivjson:
#       arrRec = xivjson["Recipes"]
#       temArr = dict()
#       for a in range(len(arrRec)):
#         recjson = api_call.apiCall(cfg.XIVRECIPE + str(arrRec[a]["ID"]))
#         rectemp = dict()
#         for b in range(10):
#           rectemp[str(recjson["ItemIngredient" + str(b) +
#                               "TargetID"])] = recjson["AmountIngredient" +
#                                                       str(b)]
#         temArr[str(arrRec[a]["ID"])] = rectemp
#       dicTemp["Recipes"] = temArr
#       DBMS.insert(dicTemp)
#   else:
#     delet = dicTemp.pop("_id")
#     DBMS.update({"_id": delet}, {"$set": dicTemp})





# def main(loopGo):

#   for i in trange(cfg.NUMLOOP):
#     temp = loopGo[0:50]
#     if len(loopGo) == 0:
#       break
#     for i in range(49):
#       loopGo.pop(0)
#     try:
#       url = cfg.UNISTART + ",".join(map(str, temp))
#       j = api_call.apiCall(url)
#       try:
#         for i in range(49):
#           dicTemp = dict()
#           dicTemp["_id"] = str(temp[i])
#           if temp[i] not in j["items"]:
#             dicTemp["price"] = 0
#             dicTemp = XIVAPIprocess(temp[i], dicTemp)
#             continue
#           elif len(j["items"][temp[i]]["listings"]) == 0:
#             dicTemp["price"] = 0
#           else:
#             dicTemp["price"] = j["items"][
#               temp[i]]["listings"][0]["pricePerUnit"]
#           # call xivitem api using temp[i] and apicall
#           dicTemp = XIVAPIprocess(temp[i], dicTemp)
#       except:
#         cfg.ERRLOG.append("Json was not readable for array" + temp[0] + " " +
#                       temp[-1])
#         print(cfg.FAIL + cfg.ERRLOG[-1] + cfg.N)
#         print(url)
#         print(dicTemp)
#         print(traceback.format_exc())
#     except Exception as err:
#       cfg.ERRLOG.append(traceback.format_exc())
#       err_handle.errExit(err)
#       print(err, temp)
#       sys.exit(traceback.format_exc())
#   print(cfg.OKGREEN + "Successfully updated market data" + cfg.N)