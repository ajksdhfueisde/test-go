from sanic import Sanic, Request
from sanic.response import text

import requests
import time

app = Sanic("MyHelloWorldApp")

def handle_id(id):
  soundfinder_url = "https://spclient.wg.spotify.com/soundfinder/v1/unauth/episode/{}/com.widevine.alpha?market=SG"
  try:
    res1 = requests.get(soundfinder_url.format(id))
    res1_data = res1.json()
    passthrough_url = res1_data.get("passthroughUrl", "")
  except BaseException:
    return ""

  if not passthrough_url:
    return ""

  def try_parser(url):
    location = url
    while True:
      print("Tring:", location)
      try:
        res2 = requests.head(location)
      except BaseException:
        time.sleep(2)
        res2 = requests.head(location)

      if res2.status_code == 302:
        location = res2.headers["location"]
      else:
        break
    return location

  source_url = try_parser(passthrough_url)
  
  return source_url
  
@app.get("/")
async def handler(request: Request):
    id = request.args.get("id")
    res = handle_id(id)
    return text(res)