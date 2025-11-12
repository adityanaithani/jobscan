import requests
import os
from dotenv import load_dotenv
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data = {
    "content" : "message content",
    "username" : "JobScan"
}

# leave this out if you dont want an embed
# for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
data["embeds"] = [
    {
        "description" : "sample job link https://www.google.ca",
        "title" : "job title"
    }
]

result = requests.post(DISCORD_WEBHOOK_URL, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print(f"Payload delivered successfully, code {result.status_code}.")

# result: https://i.imgur.com/DRqXQzA.png