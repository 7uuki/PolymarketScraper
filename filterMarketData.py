import pandas as pd
import json

# Load JSON from a file
def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def filter_empty_events(json_data):
    """
    Filters a list of JSON objects, returning only those with an empty or missing "events" attribute.

    :param json_data: List of JSON objects (list of dictionaries)
    :return: Filtered list of JSON objects
    """
    return [obj for obj in json_data if "events" not in obj or not obj["events"]]

gewünschte_felder = ["id", "title","description","volume", "tags","markets"]  # Passe diese Felder an
def to_csv(data):
    # Falls die JSON-Struktur ein Dictionary mit einer Liste ist, extrahiere die Liste-
    if isinstance(data, dict):
        data = data.get("items", data)  # Falls deine JSON eine Liste in einem Schlüssel enthält

    # Nur relevante Felder extrahieren

    # Nur relevante Felder extrahieren und tags als Label-Liste speichern
    gefilterte_daten = []
    for eintrag in data:



        eintrag_daten = {feld: eintrag.get(feld, "") for feld in gewünschte_felder}

        if "markets" in eintrag and isinstance(eintrag["markets"], list):
            if len(eintrag.get("markets")) == 1:
                eintrag_daten["markets"] = eintrag["markets"][0]["question"]
                eintrag_daten["yes"] = eintrag["markets"][0]["outcomePrices"]

            else:
                eintrag_daten["markets"] = [market["question"] for market in eintrag["markets"]]


        # Tags in ein Array von Labels umwandeln
        if "tags" in eintrag and isinstance(eintrag["tags"], list):
            eintrag_daten["tags"] = [tag["label"] for tag in eintrag["tags"]]



        gefilterte_daten.append(eintrag_daten)

    # In DataFrame umwandeln und als CSV speichern
    df = pd.DataFrame(gefilterte_daten)
    df.to_csv("daten.csv", index=False, encoding="utf-8")


def main():
    to_csv(load_json_file("data/events_20250331_191512.json"))

if __name__ == "__main__":
    main()