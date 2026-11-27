"""Shared helpers for the registry-based figures (Figs 1, 2 and 5).

The organisation lists (hyperscaler names, name-match false positives and known non-sale transfers)
are read from ``org_lists.json`` beside this file. That file is not in the repository. Copy
``org_lists.example.json`` to ``org_lists.json`` and fill it in to rebuild the registry aggregates.
The aggregates themselves are committed in ``data/``, so the figures can be redrawn without it.
"""
import json
from pathlib import Path

import pandas as pd

LISTS_PATH = Path(__file__).with_name("org_lists.json")


def load_org_lists() -> dict:
    """Return the organisation lists, or exit with a hint if the private file is missing."""
    try:
        return json.loads(LISTS_PATH.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"{LISTS_PATH} not found: copy org_lists.example.json to org_lists.json and fill it in.") from exc


def same_group(t: pd.DataFrame) -> pd.Series:
    """True where sender and recipient share a first word (a crude intra-group test)."""
    def first(col: str) -> pd.Series:
        return t[col].fillna("").str.lower().str.split().str[0]

    return first("from_org") == first("to_org")


def drop_non_sales(t: pd.DataFrame, pairs: list) -> pd.DataFrame:
    """Remove transfers matching any (sender regex, recipient regex[, note]) pair, case-insensitive."""
    sender, recipient = t.from_org.fillna("").str.lower(), t.to_org.fillna("").str.lower()
    bad = pd.Series(False, index=t.index)
    for pair in pairs:
        bad |= sender.str.contains(pair[0], regex=True) & recipient.str.contains(pair[1], regex=True)
    return t[~bad]


def market_transfers(t: pd.DataFrame, lists: dict) -> pd.DataFrame:
    """Market transfers only: drop same-group moves and the known non-sales."""
    return drop_non_sales(t[~same_group(t)], lists["non_sales"]).copy()
