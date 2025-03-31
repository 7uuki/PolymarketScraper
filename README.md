The idea is to get all polymarket Auctions compare them and find undervalued trades.
For that we're using: https://docs.polymarket.com/?python#example

At the moment [fetchMarketData](fetchMarketData.py) uses the api to fetch all events and saves them into a file in \data\

[filterMarketData](filterMarketData.py) allows you to Filter the scraped data into a csv
