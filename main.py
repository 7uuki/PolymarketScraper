import requests
import json
import sys
import time

import fetchMarketData


def main():
    fetchMarketData.fetch_and_save()

if __name__ == "__main__":
    main()