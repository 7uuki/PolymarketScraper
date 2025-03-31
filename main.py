import requests
import csv
import json
import time

def fetch_markets():
    base_url = "https://gamma-api.polymarket.com/markets"
    markets = []
    limit = 100  # Maximale Anzahl pro API-Aufruf
    offset = 0
    max_retries = 5

    while True:
        params = {"limit": limit, "offset": offset}
        retries = 0
        while retries < max_retries:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                break  # Anfrage erfolgreich
            elif response.status_code == 429:
                wait_time = 2 ** retries  # exponentiell ansteigende Wartezeit
                print(f"Rate limit erreicht (HTTP 429). Warte {wait_time} Sekunden...")
                time.sleep(wait_time)
                retries += 1
            else:
                raise Exception(f"Fehler beim Abrufen der Märkte: HTTP {response.status_code}")
        else:
            raise Exception("Maximale Anzahl an Wiederholungen erreicht bei HTTP 429.")

        data = response.json()
        if not data:
            break  # Keine weiteren Märkte vorhanden
        markets.extend(data)
        if len(data) < limit:
            break  # Letzte Seite erreicht
        offset += limit
    return markets


def main():
    all_markets = fetch_markets()
    rows = []

    for market in all_markets:
        # Filter: Nur Märkte, die aktiv sind und nicht geschlossen sind.
        if not market.get("active", False) or market.get("closed", False):
            continue

        # Titel aus "title" oder "question"
        title = market.get("title") or market.get("question", "")
        # Resolution Bedingungen aus "resolutionSource"
        resolution = market.get("resolutionSource", "")

        # Outcome-Preise (als stringifizierte Liste)
        outcome_prices_str = market.get("outcomePrices", "[]")
        try:
            prices = json.loads(outcome_prices_str)
        except Exception:
            prices = []

        # Outcome-Namen (ebenfalls als stringifizierte Liste)
        outcomes_str = market.get("outcomes", "[]")
        try:
            outcomes = json.loads(outcomes_str)
        except Exception:
            outcomes = []

        yes_price = None
        no_price = None

        # Versuche, anhand der Outcome-Namen die Preise zuzuordnen
        if isinstance(outcomes, list) and isinstance(prices, list) and len(outcomes) == len(prices):
            for outcome, price in zip(outcomes, prices):
                outcome_lower = outcome.strip().lower()
                if outcome_lower == "yes":
                    yes_price = price
                elif outcome_lower == "no":
                    no_price = price

        # Falls keine Zuordnung möglich war und es genau zwei Preise gibt:
        if yes_price is None and no_price is None and len(prices) == 2:
            yes_price, no_price = prices

        rows.append([title, yes_price, no_price, resolution])

    # Speichern der Daten in einer CSV-Datei
    with open("polymarket_markets.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Titel", "Yes Preis", "No Preis", "Resolution Bedingungen"])
        writer.writerows(rows)

    print("CSV Datei 'polymarket_markets.csv' wurde erstellt.")


if __name__ == "__main__":
    main()