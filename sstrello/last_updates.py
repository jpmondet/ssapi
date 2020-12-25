#! /usr/bin/env python3

from requests import get

SSID = "5f0eddb5738be96a56b660e7" 
BOARD_URL = f"https://api.trello.com/1/boards/{SSID}"
CARDS_INFOS = f"{BOARD_URL}/cards"


def main():
    cards_infos = get(CARDS_INFOS).json()
    sorted_cards = sorted(cards_infos, key=lambda x: x["dateLastActivity"])
    for card in sorted_cards:
        print()
        print(card["name"], card["dateLastActivity"])


if __name__ == "__main__":
    main()
