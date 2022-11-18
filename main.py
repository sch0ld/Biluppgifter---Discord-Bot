import discord # pip install discord
import requests # pip install requests
from bs4 import BeautifulSoup # pip install bs4
import re

OwnerLink = "None"
fabrikat = "None"
Fabrikat = "None"

TAG_RE = re.compile(r'<[^>]+>')


# Removes all HTML tags found in RegEx assigned above in the passed parameter and then returns it
def removeHTML(text):
	return TAG_RE.sub('', text)

#client = discord.Client()
intents = discord.Intents.all()
client = discord.Client(intents=intents)

def GetInfoAbout(reg):
  try:
    URL = 'https://biluppgifter.se/fordon/' + reg
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    ownerLink = soup.findAll("a", {"class": "gtm-merinfo"})
    OwnerLink = str(ownerLink)
    fabikat = soup.findAll("h1", {"class": "card-title"})
    fabrikat = str(fabikat)
    Fabrikat = removeHTML(fabrikat)
    Fabrikat1 = "".join(Fabrikat.splitlines())
    Fabrikat2 = Fabrikat1.replace('[', '')
    FabrikatOrig = Fabrikat2.replace(']', '')

    description = soup.findAll("img", {"src": "/images/maker/"})
    print(description)
    
    OwnerLink = "".join(OwnerLink.splitlines())

    OwnerLink1 = OwnerLink.replace("[<a class=\"gtm-merinfo\" href=\"", '')
    OwnerLink2 = OwnerLink1.replace("\" rel=\"follow\" target=\"_blank\">Visa kompletta ägaruppgifter på Merinfo.se</a>]", '')


    return ("> **Regnummer:** __" + reg + "__\n > **Fabrikat:** __" + FabrikatOrig + "__\n > **Ägare:** __" + OwnerLink2 + "__\n > **Länk till bil: **__" + "https://biluppgifter.se/fordon/" + reg.upper() + "\n > Bot Made By **TurtleBitch#5759**__")

  except Exception as e:
    return(e)


#On ready
@client.event
async def on_ready():
  
  # Prints a ready-message in the console
  print("Bot is ready as {0.user}".format(client))
  
  # Sets the "playing status"
  await client.change_presence(activity=discord.Streaming(name="Biluppgifter", url='https://biluppgifter.se'))


@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content == '$help':
    await message.channel.send("> **HELP!**\n> $help - This :P \n> ABC123")

  elif len(message.content) == 6:
    regnr = message.content.upper()
    await message.channel.send(GetInfoAbout(regnr))
    message.delete

client.run("TOKEN")