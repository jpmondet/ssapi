#! /usr/bin/env python3

from requests import get
from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List, Dict, Any

SSID: str = "5f0eddb5738be96a56b660e7" 
BOARD_URL: str = f"https://api.trello.com/1/boards/{SSID}"
CARDS_INFOS: str = f"{BOARD_URL}/cards"


def main() -> None:
    console: Console = Console()

    cards_infos: List[Dict[str, Any]] = get(CARDS_INFOS).json()

    sorted_cards: List[Dict[str, Any]] = sorted(cards_infos, key=lambda x: x["dateLastActivity"], reverse=True)

    table: Table = Table(show_header=True, header_style="bold blue")
    table.add_column("Last Updates", style="dim", width=25)
    table.add_column("Name Card")

    for index, card in enumerate(sorted_cards[:10]):
        #console.print(f"[bold cyan]{card['name']}[/bold cyan] [bold red]{card['dateLastActivity']}[/bold red]")
        last: str = card['dateLastActivity']
        name: Text = Text(card['name'])
        if index == 0:
            name.stylize("bold green")
            last = f"[bold cyan]{card['dateLastActivity']}[/bold cyan]"
        table.add_row(last, name)

    console.print()
    console.print("[bold white underline]ScoreSaber's Trello updates")
    console.print(table)


if __name__ == "__main__":
    main()
