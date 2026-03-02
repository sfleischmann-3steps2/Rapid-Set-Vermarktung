#!/usr/bin/env python3
"""
Anreicherung der ARM_ADM_Gesamtliste.csv mit Straßenadressen via Impressum-Scraping.

Logik je Zeile:
  1. Domain aus Email extrahieren
  2. URL-Kandidaten probieren (/impressum, /kontakt, etc.)
  3. Bekannte PLZ im Text suchen (Cross-Validation)
  4. Zeile vor der PLZ = Straße + Hausnummer
  5. Ergebnis in ARM_ADM_Gesamtliste_enriched.csv schreiben

Checkpoint-Datei enrich_checkpoint.json erlaubt Resume nach Abbruch.
"""

import csv
import re
import json
import time
import os
import sys
import io
import html
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "ARM_ADM_Gesamtliste_enriched.csv")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, "enrich_checkpoint.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "de-DE,de;q=0.9,en;q=0.5",
}

REQUEST_TIMEOUT = 10
RATE_LIMIT_DELAY = 1.0  # seconds between requests

# Straßen-Regex: Großbuchstabe + Kleinbuchstaben + Straßensuffix + Hausnummer
STREET_PATTERN = re.compile(
    r"[A-ZÄÖÜ][a-zäöüß\-]+(?:straße|str\.|weg|gasse|allee|platz|ring|damm|chaussee|promenade|ufer|graben)\s+\d+[a-zA-Z]?",
    re.IGNORECASE,
)

# Postleitzahl-Regex (5-stellig, Deutschland)
PLZ_PATTERN = re.compile(r"\b(\d{5})\b")


def extract_domain(email: str) -> str:
    """Extrahiert die Domain aus einer E-Mail-Adresse."""
    email = email.strip().lower()
    if "@" not in email:
        return ""
    return email.split("@", 1)[1].strip()


def fetch_url(url: str) -> str | None:
    """Lädt eine URL und gibt den Text-Inhalt zurück. None bei Fehler."""
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            content_type = resp.headers.get("Content-Type", "")
            charset = "utf-8"
            ct_match = re.search(r"charset=([^\s;]+)", content_type)
            if ct_match:
                charset = ct_match.group(1).strip().strip('"')
            raw = resp.read()
            try:
                return raw.decode(charset, errors="replace")
            except (LookupError, UnicodeDecodeError):
                return raw.decode("utf-8", errors="replace")
    except (HTTPError, URLError, OSError):
        return None
    except Exception:
        return None


def strip_html_tags(text: str) -> str:
    """Entfernt HTML-Tags und dekodiert HTML-Entities."""
    text = html.unescape(text)
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def find_address_in_text(text: str, plz: str) -> str:
    """
    Sucht nach Straße in der Nähe der bekannten PLZ.
    Gibt Straße+Hausnummer zurück oder "".
    """
    # PLZ im Text suchen
    plz_match = PLZ_PATTERN.search(text)
    if not plz_match:
        return ""

    # Alle PLZ-Positionen finden, nach bekannter PLZ filtern
    found_pos = -1
    for m in PLZ_PATTERN.finditer(text):
        if m.group(1) == plz:
            found_pos = m.start()
            break

    if found_pos == -1:
        return ""

    # Kontext um die PLZ herum (300 Zeichen davor, 50 danach)
    context_start = max(0, found_pos - 300)
    context = text[context_start : found_pos + 50]

    # Straße in diesem Kontext suchen
    street_matches = list(STREET_PATTERN.finditer(context))
    if street_matches:
        # Letzten Treffer vor der PLZ nehmen (der ist am nächsten)
        best = street_matches[-1].group(0).strip()
        return best

    return ""


def build_url_candidates(domain: str) -> list[str]:
    """Gibt URL-Kandidaten in Prioritätsreihenfolge zurück."""
    candidates = [
        f"https://www.{domain}/impressum",
        f"https://www.{domain}/impressum.html",
        f"https://www.{domain}/impressum/",
        f"https://www.{domain}/kontakt",
        f"https://www.{domain}/kontakt.html",
        f"https://www.{domain}/kontakt/",
        f"https://www.{domain}",
        f"https://{domain}/impressum",
        f"https://{domain}/impressum.html",
        f"https://{domain}",
    ]
    return candidates


def scrape_address(email: str, plz: str) -> tuple[str, str]:
    """
    Scrapt Adresse für eine E-Mail/PLZ-Kombination.
    Gibt (straße, status) zurück: status ist 'found' oder 'not_found'.
    """
    domain = extract_domain(email)
    if not domain:
        return "", "not_found"

    for url in build_url_candidates(domain):
        raw_html = fetch_url(url)
        if not raw_html:
            time.sleep(0.2)
            continue

        text = strip_html_tags(raw_html)
        straße = find_address_in_text(text, plz)

        time.sleep(RATE_LIMIT_DELAY)

        if straße:
            return straße, "found"

        # Nur kurz warten zwischen Kandidaten derselben Domain
        time.sleep(0.3)

    return "", "not_found"


def load_checkpoint() -> dict:
    """Lädt vorhandenen Checkpoint oder gibt leeres Dict zurück."""
    if os.path.exists(CHECKPOINT_FILE):
        try:
            with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_checkpoint(checkpoint: dict) -> None:
    """Speichert Checkpoint-Dict als JSON."""
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def enrich() -> None:
    checkpoint = load_checkpoint()
    print(f"Checkpoint geladen: {len(checkpoint)} bereits verarbeitete Einträge")

    # Quelldaten einlesen
    with open(INPUT_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    print(f"Eingabe: {len(rows)} Zeilen aus {os.path.basename(INPUT_FILE)}")

    # Ausgabe-Spalten
    out_fieldnames = list(fieldnames) + ["Straße", "Adresse_Status"]

    found_count = 0
    not_found_count = 0
    total = len(rows)

    enriched_rows = []

    for i, row in enumerate(rows, start=1):
        email = row.get("Email", "").strip()
        plz = row.get("PLZ", "").strip()
        firma = row.get("Firma", "").strip()

        # Checkpoint-Key: E-Mail (eindeutig genug)
        ck_key = email if email else f"row_{i}"

        if ck_key in checkpoint:
            # Aus Checkpoint laden
            cached = checkpoint[ck_key]
            straße = cached.get("straße", "")
            status = cached.get("status", "not_found")
            symbol = "✓" if status == "found" else "✗"
            print(f"  [{i:3d}/{total}] {symbol} [CACHE] {firma[:35]:<35} → {straße or '—'}")
        else:
            # Scrapen
            print(f"  [{i:3d}/{total}]   Scrape: {firma[:35]:<35} ({email})", end="", flush=True)

            if not email or "@" not in email:
                straße, status = "", "not_found"
            else:
                straße, status = scrape_address(email, plz)

            symbol = "✓" if status == "found" else "✗"
            print(f"\r  [{i:3d}/{total}] {symbol} {firma[:35]:<35} → {straße or '—'}")

            # Checkpoint speichern
            checkpoint[ck_key] = {"straße": straße, "status": status}
            save_checkpoint(checkpoint)

        if status == "found":
            found_count += 1
        else:
            not_found_count += 1

        enriched_row = dict(row)
        enriched_row["Straße"] = straße
        enriched_row["Adresse_Status"] = status
        enriched_rows.append(enriched_row)

    # Ausgabe schreiben
    with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(enriched_rows)

    print()
    pct_found = found_count / total * 100 if total > 0 else 0
    pct_not = not_found_count / total * 100 if total > 0 else 0
    print(f"✓  Gefunden:       {found_count:3d} / {total} ({pct_found:.0f}%)")
    print(f"✗  Nicht gefunden: {not_found_count:3d} / {total} ({pct_not:.0f}%)")
    print(f"→  Ausgabe: {os.path.basename(OUTPUT_FILE)}")


if __name__ == "__main__":
    enrich()
