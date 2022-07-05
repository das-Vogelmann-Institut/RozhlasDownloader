from base64 import encode
import requests as r
from bs4 import BeautifulSoup as bs

import typer
import eyed3
import UserAgents as ua
import random
import json
import os
import shutil

def createUserAgents():
    return f"User-Agent : ${ua.UserAgents[random.randint(0,len(ua.UserAgents)-1)]}"

def get(url):
    headers = createUserAgents()
    page = r.get(url,headers)
    return page

def soup(page):
    return bs(page.content, 'html.parser')

def to_latin(title):
    title = title.lower()
    # ěščřžýáíéúůňťďó
    prohibited_chars = "ěščřžýáíéúůňťďó"
    allowed_chars = "escrzyaieuuntdo"
    for old, new in zip(prohibited_chars,allowed_chars):
        title = title.replace(old,new)
    return title

def edit_metadata(title, number):
    audiofile = eyed3.load(f"{title}.mp3")
    title = to_latin(title)
    audiofile.tag.artist = title
    audiofile.tag.album = "Stolen GOODS"
    audiofile.tag.album_artist = "Rozhlas.cz"
    audiofile.tag.title = title
    audiofile.tag.track_num = number
    audiofile.tag.save()

global dump

def download_file(url):
    global dump

    file = r.get(url, stream=True)
    dump = file.raw

def save_file(title):
    global dump
    location = os.path.abspath("./downloads")
    with open(f"{title}.mp3", 'wb') as location:
        shutil.copyfileobj(dump, location)
    del dump
    

def Main(source: str):
    typer.echo(to_latin("Jak vzniká oscilátor a jak se používá sekvencer? Ondřej Bambas se vydává do dílny hudebníka a vynálezce nástrojů Václava Pelouška"))
    typer.secho(f"Downloading from Rozhlas | {source}",fg=typer.colors.MAGENTA, bold=True, bg = typer.colors.WHITE)
    bs = soup(get(source))
    data = bs.find_all("div", class_="mujRozhlasPlayer")[0].get("data-player")
    jsondata = json.loads(data)
    playlist = jsondata.get("data").get("playlist")
    number = 0
    for episode in playlist:
        name = episode.get("title")
        url = episode.get("audioLinks")[0].get("url")
        download_file(url)
        save_file(name)
        typer.echo(f"\n{name} downloaded!")
        edit_metadata(name,number)
        typer.echo(f"\n{name} has new cool metadata!")
        number = number + 1
   
    typer.secho("Done! Hope it brightens your day!", fg=typer.colors.GREEN, bold=True)

if __name__ == "__main__":
    typer.run(Main)
