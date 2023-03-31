import traceback
from discord_webhook import DiscordWebhook
import cfg

def rprt(type):
  if type == "ERROR":
    print("[ERROR] " + traceback.format_exc())
    post_message("[ERROR] " + traceback.format_exc())
  else:
    pass

def post_message(message):
  try:
    webhook = DiscordWebhook(url=cfg.WEBHOOK, content=message)
    webhook.execute()
  except:
    pass

