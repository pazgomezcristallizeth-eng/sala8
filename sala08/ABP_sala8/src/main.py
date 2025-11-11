import flet as ft
from urllib.parse import urlparse

GUINDA = "#8"


def to_raw_github(url: str) -> str:
    if not url:
        return url
    p =urlparse(url)
    if "github.com" in p.netloc and "/blob/" in p.path:
        parts = p.path.strip("/").strip("/")
        if len(parts) >= 5 and parts[2] == "blod":
            user, repo, _, branch, *rest = parts
            return f"https://raw.githubusercontent"


def main(page: ft.Page):
    
    
ft.app(main)
