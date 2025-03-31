import json
import sys
import time
from datetime import datetime
import requests

def write_refresh(string):
    sys.stdout.write(f"\r{string}")
    sys.stdout.flush()

def fetch_markets(limit=100, max_retries=5):
    base_url = "https://gamma-api.polymarket.com/events"
    print(f"Started fetching from {base_url}")
    offset = 0

    markets = []

    while True:
        params = {"limit": limit, "offset": offset, "archived": False, "closed": False, "active": True}
        retries = 0
        while retries < max_retries:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                break  # Anfrage erfolgreich
            elif response.status_code == 429:
                wait_time = 2 ** retries  # exponentiell ansteigende Wartezeit
                write_refresh(f"Rate limit reached (HTTP 429). Wait for {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                raise Exception(f"Fehler beim Abrufen der Märkte: HTTP {response.status_code}")
        else:
            raise Exception("Maximale Anzahl an Wiederholungen erreicht bei HTTP 429.")

        data = response.json()  # Antwort als JSON
        if not data:  # Falls keine neuen Daten kommen, abbrechen
            break

        markets.extend(data)  # Daten zur Liste hinzufügen

        write_refresh(f"Fetching data... ({limit + offset} Markets)")

        offset += limit  # Offset erhöhen

    write_refresh(f"Successfully finished fetching ({len(markets)} items)!\n")
    return markets

def save_markets(markets):
    filename = f"data/events_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
    # Speichern der gesammelten Daten in einer JSON-Datei
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(markets, file, indent=4, ensure_ascii=False)
    print(f"Saved {len(markets)} Markets to {filename}")


def fetch_and_save():
    save_markets(fetch_markets())

if __name__ == "__main__":
    fetch_and_save()
