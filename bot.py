import discord
import base64
from discord.ext import commands, tasks
import datetime
import discord, datetime, time, aiohttp, asyncio, random
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import asyncio
import time

bot = commands.Bot(command_prefix='!')

async def status_task():
    print("works! :)")
    while True:
        channel = bot.get_channel(755676196804755466)
        await channel.send(get_latest_message())
        await asyncio.sleep(86400)
        await channel.send(get_latest_message())
        await asyncio.sleep(86400)

@bot.event
async def on_ready():
    bot.loop.create_task(status_task())


def get_latest_message():
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'new_client_secret.json', SCOPES)
          creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  service = build('gmail', 'v1', credentials=creds)

  # Call the Gmail API

  results = service.users().messages().list(userId='me').execute()
  messages = results.get('messages', [])

  msgs = []
  message_count = 1
  for message in messages[:1]:
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    msgs.append(str(base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data']).decode("utf-8") )) 
    print(str(msgs[0]))
  msgs[0] = msgs[0].replace('\r\n', '\n')
  print(msgs[0])
  parts = msgs[0].split("------------------------------")
  print(parts[0])
  return parts[0]

@bot.command()
@commands.has_role('Officers')
async def message(ctx):
  await ctx.send(get_latest_message())



bot.run('token')
