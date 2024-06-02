from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests



def search_discovery_plus(query):
    url = f"https://www.discoveryplus.in/search/all/{query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for item in soup.find_all("div", class_="card-content"):
        title = item.find("h4", class_="card-title").text.strip()
        description = item.find("div", class_="card-description").text.strip()
        results.append({"title": title, "description": description})
    return results


@Client.on_message(filters.command("restart"))
def restart(client, message):
    message.reply_text("Welcome to Discovery Plus OTT show search bot! Send /search <query> to find shows.")


@Client.on_message(filters.command("search"))
def search(client, message):
    query = " ".join(message.command[1:])
    if not query:
        message.reply_text("Please provide a query to search for.")
        return
    results = search_discovery_plus(query)
    if results:
        for result in results:
            response_text = f"<b>{result['title']}</b>\n{result['description']}"
            message.reply_text(response_text, parse_mode="html")
    else:
        message.reply_text("No results found.")


